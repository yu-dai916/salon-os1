from datetime import date
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Store
from app.models_keywords import Keyword, StoreKeyword
from app.models_metrics import Metric
from app.services.google_rank import get_google_rank


def run():
    db: Session = SessionLocal()

    rows = (
        db.query(StoreKeyword, Keyword, Store)
        .join(Keyword, Keyword.id == StoreKeyword.keyword_id)
        .join(Store, Store.id == StoreKeyword.store_id)
        .all()
    )

    for sk, k, store in rows:
        base_keyword = k.keyword
        area = (store.station or "").replace("駅", "").strip()

        if area:
            search_keyword = f"{area} {base_keyword}"
        else:
            search_keyword = base_keyword

        rank = get_google_rank(search_keyword, "hotpepper.jp")

        existing = (
            db.query(Metric)
            .filter(
                Metric.store_id == store.id,
                Metric.keyword == search_keyword,
                Metric.metric_date == date.today(),
            )
            .first()
        )

        if existing:
            existing.google_rank = rank
        else:
            m = Metric(
                store_id=store.id,
                keyword=search_keyword,
                metric_date=date.today(),
                google_rank=rank,
            )
            db.add(m)

        print(f"[rank] store:{store.id} {search_keyword} -> {rank}")

    db.commit()
    db.close()