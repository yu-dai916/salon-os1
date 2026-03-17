from fastapi import APIRouter
from app.services.ai_strategy import analyze_competition

router = APIRouter(prefix="/competition-ai")

@router.get("/")
def competition_ai():

    result = analyze_competition(
        store_rank=5,
        competitor_rank=2,
        reviews=30,
        competitor_reviews=80,
        posts=4
    )

    return {"advice": result}