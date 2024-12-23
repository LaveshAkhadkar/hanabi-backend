from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from app.services.sentiment_analysis import analyze_sentiments
from app.core.security import get_current_user
import pandas as pd

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


@router.post("/analyze")
async def analyze_csv(
    file: UploadFile = File(...), current_user: str = Depends(get_current_user)
):
    """
    Endpoint to analyze sentiment from a CSV file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only CSV files are supported."
        )

    try:
        df = pd.read_csv(file.file)

        # Ensure required columns exist
        if "id" not in df.columns or "text" not in df.columns:
            raise HTTPException(
                status_code=400, detail="Missing required columns: 'id', 'text'"
            )

        # Perform sentiment analysis
        analyzed_df = analyze_sentiments(df)

        # Convert the DataFrame to JSON
        result_json = analyzed_df.to_dict(orient="records")
        return {"user": current_user, "results": result_json}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
