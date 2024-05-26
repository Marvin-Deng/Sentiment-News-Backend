import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_URL = os.getenv("CLIENT_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
TINNGO_API_KEY = os.getenv("TIINGO_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
