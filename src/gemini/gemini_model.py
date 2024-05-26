import os
from dotenv import load_dotenv
import google.generativeai as genai

from constants.sentiment import SENTIMENT_OPTIONS

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_KEY"))
model = genai.GenerativeModel("gemini-pro")


def gemini_analyze_sentiment(text):
    try:
        prompt = f"Analyze the sentiment of the following text using only one of the following: {SENTIMENT_OPTIONS}. {text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return None
