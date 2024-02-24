Sentiment = {
    "Positive": ["Optimistic", "Positive", "Stable"],
    "Negative": ["Pessimistic", "Negative", ],
    "Neutral": ["Inconsistent", "Cautious", "Neutral"]
}

SENTIMENT_MAP = {
    "Positive": frozenset(Sentiment.get("Positive")),
    "Negative": frozenset(Sentiment.get("Negative")),
    "Neutral": frozenset(Sentiment.get("Neutral"))
}

SENTIMENT_OPTIONS = ', '.join([sentiment for category in Sentiment.values() for sentiment in category])