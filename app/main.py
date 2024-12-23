from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.sentiment_analysis import router as sentiment_router
from app.api.routes.auth import router as auth_router


app = FastAPI()

app.include_router(sentiment_router)
app.include_router(auth_router)

origins = [
    "*",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "healthy"}