from transformers import pipeline, AutoTokenizer, logging
import pandas as pd


logging.set_verbosity_error()

sentiment_task = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)
tokenizer = AutoTokenizer.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest"
)

MAX_TOKENS = 500



def analyze_sentiment(description):
    """
    Analyze the sentiment of a description using Hugging Face's sentiment analysis pipeline.
    """

    tokenized_description = tokenizer.encode(description)
    if len(tokenized_description) > MAX_TOKENS:

        shortened_description = tokenizer.decode(tokenized_description[:MAX_TOKENS])
    else:
        shortened_description = description

    try:
        result = sentiment_task(shortened_description)

        return result[0]["label"]
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Error"


def analyze_sentiments(input_file, output_file):
    """
    Read the CSV, analyze the sentiment of descriptions, and save the results.
    """
    df = pd.read_csv(input_file)
    if "Description" not in df.columns:
        print("No 'Description' column found in input file.")
        return

    sentiments = []
    for description in df["Description"]:
        sentiments.append(analyze_sentiment(description))

    df["Sentiment"] = sentiments
    df.to_csv(output_file, index=False)
