from fastapi import APIRouter
from app.services.post_ai_service import generate_google_post_from_blog
from app.db import SessionLocal
from app.models.store import Store

router = APIRouter()


@router.post("/posts/ai_generate")
def ai_generate(store_id: int, title: str, content: str):
    db = SessionLocal()

    store = db.query(Store).get(store_id)

    result = generate_google_post_from_blog(
        title=title,
        excerpt=content,
        source_url="",
        strategy_key=store.strategy_key,
        phone_number=store.phone_number,
        cta_url=store.cta_url,
        store_name=store.name,
        area=store.area,
        main_menu=store.main_menu,
    )

    return {"result": result}