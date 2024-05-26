import google.generativeai as genai

from constants.sentiment import SENTIMENT_OPTIONS
from constants.env_consts import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")


def gemini_analyze_sentiment(text):
    try:
        prompt = f"Analyze the sentiment of the following text using only one of the following: {SENTIMENT_OPTIONS}. {text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return None
