from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os

from openai import OpenAI

from app.db import get_db
from app.models.review import Review
from app.models.store import Store

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.post("/reviews/{review_id}/quick_reply")
def quick_reply(review_id: int, db: Session = Depends(get_db)):

    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        return {"error": "not found"}

    store = db.query(Store).filter(Store.id == review.store_id).first()

    staff = getattr(review, "staff_name", None) or "担当スタッフ"
    menu = getattr(review, "menu_name", None) or "施術"
    area = store.name if store else "美容室"

    keyword = f"{area} {menu}"

    prompt = f"""
美容室のGoogle口コミ返信を作成してください。

口コミ:
{review.comment or ""}

条件:
・丁寧
・来店のお礼
・次回来店につながる一言
・自然な日本語
・必ず「{staff}」として返信
・「{menu}」に触れる
・「{keyword}」を自然に1回だけ含める
・120文字以内
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        reply = response.choices[0].message.content.strip()

        # 空対策
        if not reply:
            raise Exception("empty reply")

    except Exception:
        reply = f"{staff}です。{menu}でのご来店ありがとうございました！またのご来店を心よりお待ちしております。"

    review.reply_text = reply
    review.replied_at = datetime.utcnow()

    db.commit()

    return RedirectResponse(
        url=f"/store/{review.store_id}/reviews",
        status_code=303
    )