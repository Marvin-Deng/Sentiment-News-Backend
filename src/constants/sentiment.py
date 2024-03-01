SENTIMENT = {
    "Positive": ["Optimistic", "Positive", "Stable"],
    "Negative": ["Pessimistic", "Negative", ],
    "Neutral": ["Inconsistent", "Cautious", "Neutral"]
}

SENTIMENT_MAP = {
    "Positive": SENTIMENT.get("Positive"),
    "Negative": SENTIMENT.get("Negative"),
    "Neutral": SENTIMENT.get("Neutral")
}

SENTIMENT_OPTIONS = ', '.join([sentiment for category in SENTIMENT.values() for sentiment in category])