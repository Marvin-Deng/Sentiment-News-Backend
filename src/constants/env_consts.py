import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_URL = os.getenv("CLIENT_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
TINNGO_API_KEY = os.getenv("TIINGO_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

FINNHUB_KEY_1 = os.getenv("FINNHUB_KEY_1")
FINNHUB_KEY_2 = os.getenv("FINNHUB_KEY_2")
FINNHUB_KEY_3 = os.getenv("FINNHUB_KEY_3")
FINNHUB_KEY_4 = os.getenv("FINNHUB_KEY_4")
FINNHUB_KEY_5 = os.getenv("FINNHUB_KEY_5")
