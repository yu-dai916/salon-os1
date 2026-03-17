from sqlalchemy.orm import Session
from datetime import datetime

from app.db import SessionLocal
from app.models import Store
from app.models_metrics import Metric
from app.services.ga4 import get_hpb_clicks


def run():

    db: Session = SessionLocal()

    stores = db.query(Store).all()

    clicks = get_hpb_clicks()

    for store in stores:

        m = Metric(
            store_id=store.id,
            metric_date=datetime.utcnow().date(),
            hpb_clicks=clicks
        )

        db.add(m)

    db.commit()
    db.close()