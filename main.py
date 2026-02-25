from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI()

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    rating: int

def analyze_sentiment(comment: str) -> SentimentResponse:
    comment_lower = comment.lower()
    positive_words = ["amazing", "love", "great", "excellent", "perfect", "awesome", "good", "fantastic", "best"]
    negative_words = ["sucks", "hate", "terrible", "worst", "bad", "horrible", "awful", "trash"]
    
    if any(word in comment_lower for word in positive_words):
        return {"sentiment": "positive", "rating": 5}
    elif any(word in comment_lower for word in negative_words):
        return {"sentiment": "negative", "rating": 1}
    else:
        return {"sentiment": "neutral", "rating": 3}

# POST /comment (assignment requirement)
@app.post("/comment", response_model=SentimentResponse)
async def post_comment(request: CommentRequest):
    return analyze_sentiment(request.comment)

# GET /comment - FIXED for testers
@app.get("/comment", response_model=SentimentResponse)
async def get_comment(comment: Optional[str] = Query(None)):
    if not comment or not comment.strip():
        raise HTTPException(status_code=400, detail="Missing required 'comment' parameter")
    return analyze_sentiment(comment)

@app.get("/")
async def root():
    return {"message": "Sentiment Analysis API Ready!"}
