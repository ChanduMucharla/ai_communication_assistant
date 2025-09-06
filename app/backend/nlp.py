
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

_vader = None

def ensure_vader():
    global _vader
    if _vader is None:
        try:
            _vader = SentimentIntensityAnalyzer()
        except Exception:
            nltk.download('vader_lexicon')
            _vader = SentimentIntensityAnalyzer()
    return _vader

def sentiment_label(text: str) -> str:
    sia = ensure_vader()
    s = sia.polarity_scores(text or "")
    compound = s.get("compound", 0.0)
    if compound >= 0.25:
        return "Positive"
    elif compound <= -0.25:
        return "Negative"
    return "Neutral"
