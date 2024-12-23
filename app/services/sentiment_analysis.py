import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
headers = {"Authorization": os.environ.get("HUGGINGFACE_API_KEY")}


def query(payload):
    """
    Query the Hugging Face API with the given payload.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for HTTP issues
    return response.json()

def analyze_sentiment_batch(texts):
    """
    Perform sentiment analysis on a batch of texts.
    """
    sentiments = []
    for text in texts:
        output = query({"inputs": text})
        if output and isinstance(output, list) and len(output) > 0:
            # Extract the first element (list of scores) and find the max score
            sentiment_scores = output[0]  # Get the first list of dictionaries
            if isinstance(sentiment_scores, list):
                # Find the label with the highest score
                best_sentiment = max(sentiment_scores, key=lambda x: x["score"])
                sentiments.append(best_sentiment["label"])
            else:
                sentiments.append("ERROR")
        else:
            sentiments.append("ERROR")  # Fallback for unexpected response structure
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
    df["sentiment"] = sentiments
    return df