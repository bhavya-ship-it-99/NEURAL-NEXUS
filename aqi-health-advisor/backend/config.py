import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WAQI_TOKEN = os.getenv("WAQI_TOKEN")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    print(f"WARNING: GROQ_API_KEY not set in {ENV_FILE}")

if not WAQI_TOKEN:
    print(f"WARNING: WAQI_TOKEN not set in {ENV_FILE}")
