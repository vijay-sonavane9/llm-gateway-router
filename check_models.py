import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load your .env file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: Could not find GROQ_API_KEY in your .env file.")
    exit()

print("Fetching available models from Groq...")
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)

if response.status_code == 200:
    models = response.json().get("data", [])
    print("\n✅ Your API Key has access to these EXACT model strings:\n")
    for m in models:
        print(f"  - {m['id']}")
    print("\nPick a fast/cheap one for Tiers 0 and 1, and a heavy/smart one for Tier 2.")
else:
    print(f"❌ API Error: {response.status_code} - {response.text}")