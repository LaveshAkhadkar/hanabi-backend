from fastapi import APIRouter, HTTPException




router = APIRouter("/sentiment_analysis", tags=["sentiment_analysis"])

#Route to accept a csv file and return tabular data with sentiment analysis to frontend
