from fastapi import APIRouter
from app.services.ai_reply_service import generate_reply

router = APIRouter(prefix="/ai")


@router.post("/reply")
def ai_reply(review_text: str):

    reply = generate_reply(review_text)

    return {"reply": reply}