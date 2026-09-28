from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "router.pkl"
DB_PATH = BASE_DIR / "metrics.db"

# Force Python to read your .env file
load_dotenv(BASE_DIR / ".env")

# Now it will successfully pull your key from the .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Make sure it is saved in your .env file.")

# Using the EXACT models your specific Groq account has access to
PROVIDER_CONFIG = {
    0: {"model": "openai/gpt-oss-20b"},    # Fast model for Easy tasks
    1: {"model": "openai/gpt-oss-20b"},    # Fast model for Medium tasks
    2: {"model": "openai/gpt-oss-120b"}    # Heavy model for Hard tasks
}