import streamlit as st
import pandas as pd
import sqlite3
import requests
from pathlib import Path

st.set_page_config(page_title="LLM Smart Router Demo", layout="wide")

# Paths & Endpoints
DB_PATH = Path(__file__).resolve().parent.parent / "metrics.db"
FASTAPI_URL = "http://localhost:8000/v1/chat/completions"

st.title("🔀 Smart LLM Cost Router")
st.markdown("This system intercepts prompts, classifies their complexity using a Scikit-Learn model, and routes them to the cheapest capable LLM.")

# Split the screen into two columns
col_chat, col_dash = st.columns([1, 1], gap="large")

# ==========================================
# LEFT COLUMN: INTERACTIVE CHAT
# ==========================================
with col_chat:
    st.subheader("💬 Test the Router")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "model" in msg:
                st.caption(f"🚀 **Routed to:** `{msg['model']}` (Tier {msg['tier']})")

    # Chat Input Box
    if prompt := st.chat_input("Ask something (e.g., 'What is 2+2?')"):
        
        # Add user message to UI
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Send request to your FastAPI Gateway
        with st.chat_message("assistant"):
            with st.spinner("Evaluating prompt complexity..."):
                payload = {"messages": [{"role": "user", "content": prompt}]}
                try:
                    response = requests.post(FASTAPI_URL, json=payload, timeout=60)
                    data = response.json()
                    
                    # Safely check if 'choices' exists in the response
                    if "choices" in data:
                        reply = data["choices"][0]["message"]["content"]
                        model_used = data.get("model", "unknown-model")
                        
                        tier = "2 (Hard)" if "120b" in model_used else "0/1 (Easy/Medium)"
                        
                        st.markdown(reply)
                        st.caption(f"🚀 **Routed to:** `{model_used}` (Tier {tier})")
                        
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": reply, 
                            "model": model_used,
                            "tier": tier
                        })
                        
                        # Automatically refresh the page to update the dashboard metrics on the right
                        st.rerun()
                    else:
                        error_msg = data.get('error', {}).get('message', str(data))
                        st.error(f"Groq API Error: {error_msg}")
                        st.caption("Check your GROQ_API_KEY in the terminal running FastAPI.")

                except Exception as e:
                    st.error(f"Failed to connect to FastAPI. Is the server running? Error: {str(e)}")

# ==========================================
# RIGHT COLUMN: LIVE OBSERVABILITY DASHBOARD
# ==========================================
with col_dash:
    st.subheader("📊 Live System Metrics")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM routing_logs", conn)
        conn.close()
    except Exception:
        df = pd.DataFrame()

    if df.empty:
        st.info("Waiting for traffic... Send a message in the chat to see metrics.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Requests", len(df))
        m2.metric("Router Overhead", f"{df['routing_latency_ms'].mean():.2f} ms")
        
        # Calculate estimated savings: routing to 20B saves ~$0.002 per prompt vs 120B
        routed_away = len(df[df['tier'] < 2])
        savings_dollars = routed_away * 0.002
        m3.metric("Estimated Cost Savings", f"${savings_dollars:.4f}")

        # Visualizations
        st.markdown("**Traffic by Target Model**")
        
        if 'model_used' in df.columns:
            chart_data = df['model_used'].value_counts()
            chart_data.index = chart_data.index.astype(str)
            st.bar_chart(chart_data)
        
        st.markdown("**Recent Routing Logs**")
        if not df.empty:
            display_df = df.tail(5)[['timestamp', 'tier', 'model_used', 'routing_latency_ms']]
            display_df = display_df.sort_values(by="timestamp", ascending=False)
            st.dataframe(display_df, use_container_width=True)