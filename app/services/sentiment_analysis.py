from transformers import pipeline, AutoTokenizer, logging
import pandas as pd

logging.set_verbosity_error()

# Load model and tokenizer
sentiment_task = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)
tokenizer = AutoTokenizer.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest"
)

MAX_TOKENS = 500


def analyze_sentiment_batch(texts):
    """
    Perform sentiment analysis on a batch of texts after truncating each to 500 tokens.
    """

    # Truncate each text to 500 tokens
    truncated_texts = [
        tokenizer.decode(
            tokenizer.encode(text, max_length=MAX_TOKENS, truncation=True),
            skip_special_tokens=True,
        )
        for text in texts
    ]

    # Perform sentiment analysis
    sentiments = sentiment_task(truncated_texts)
    return sentiments


def analyze_sentiments(df: pd.DataFrame):
    """
    Analyze sentiments for the input DataFrame and return with sentiment results.
    """
    # Ensure required columns exist
    if "id" not in df.columns or "text" not in df.columns:
        raise ValueError("Missing required columns: 'id', 'text'")

    # Perform sentiment analysis
    sentiments = analyze_sentiment_batch(df["text"])
    sentiment_labels = [result["label"] for result in sentiments]

    # Add sentiment results to the DataFrame
    df["sentiment"] = sentiment_labels
    return df
