"""
Module for sentiment analysis using Gemini.
"""

import google.generativeai as genai

from constants.sentiment import SENTIMENT_OPTIONS
from constants.env_consts import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-pro")


def gemini_analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of the provided text using Gemini.
    """
    try:
        prompt = (
            f"Analyze the sentiment of the following text using only one of the following: "
            f"{SENTIMENT_OPTIONS}. {text}"
        )
        response = MODEL.generate_content(prompt)
        return response.text

    except Exception:
        return None
