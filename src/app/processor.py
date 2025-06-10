"""Processor module for news sentiment analysis.

This module analyzes the sentiment of incoming news content using TextBlob.
It extracts a polarity score and classifies the sentiment into
'positive', 'neutral', or 'negative'.
"""

from typing import Any

from textblob import TextBlob

from app.utils.setup_logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def analyze_sentiment(data: dict[str, Any]) -> dict[str, Any]:
    """Analyzes sentiment of news content.

    Args:
        data (dict[str, Any]): A dictionary containing at least a 'headline' or 'content' key.

    Returns:
        dict[str, Any]: The input dictionary with 'sentiment_score' and 'sentiment_label' added.

    """
    content = data.get("headline") or data.get("content")

    if not content:
        logger.warning("No text found for sentiment analysis.")
        data["sentiment_score"] = None
        data["sentiment_label"] = "unknown"
        return data

    try:
        analysis = TextBlob(content)
        sentiment: Any = analysis.sentiment  # For Pyright compatibility
        polarity = sentiment.polarity

        data["sentiment_score"] = polarity
        data["sentiment_label"] = classify_sentiment(polarity)

        logger.info("Sentiment analysis complete: %.2f (%s)", polarity, data["sentiment_label"])
        return data

    except Exception as e:
        logger.error("Sentiment analysis failed: %s", e)
        data["sentiment_score"] = None
        data["sentiment_label"] = "error"
        return data


def classify_sentiment(score: float) -> str:
    """Classifies polarity score into sentiment label.

    Args:
        score (float): Polarity score from -1.0 to 1.0.

    Returns:
        str: One of 'positive', 'neutral', or 'negative'.

    """
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    return "neutral"
