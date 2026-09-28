import time
import httpx
import pickle
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from src.extractor import extract_features
from src.config import MODEL_PATH, PROVIDER_CONFIG, GROQ_API_KEY
from src.db import log_request

app = FastAPI(title="LLM Cost Router Gateway")

with open(MODEL_PATH, "rb") as f:
    router_model = pickle.load(f)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest, background_tasks: BackgroundTasks):
    user_messages = [m.content for m in req.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message found.")
    
    start_time = time.perf_counter()
    
    # 1. Predict tier (0, 1, or 2)
    features = extract_features(user_messages[-1])
    tier = int(router_model.predict(features)[0])
    
    routing_latency = (time.perf_counter() - start_time) * 1000
    target = PROVIDER_CONFIG[tier]
    
    # 2. Log silently in the background (No SQL required by you)
    background_tasks.add_task(log_request, tier, target["model"], routing_latency)
    
    # 3. Forward request to Groq's Free API
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": target["model"], "messages": [m.dict() for m in req.messages]}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        return response.json()