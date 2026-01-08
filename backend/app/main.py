from fastapi import FastAPI

from app.domain.auth.api import router as auth_router
from app.domain.admin.api import router as admin_router
from app.domain.trade.api import router as trade_router


from app.db.session import engine
from app.db.base import Base
from app.models import user, settings  # noqa: F401  (테이블 등록용)

from app.models import user, settings, referral, commission  # noqa: F401

app = FastAPI(title="SellAndBuyCo API", version="0.1.0")

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(trade_router)

# DB 테이블 생성 (MVP)
Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.referral import ReferralRule

def seed_referral_rules():
    with Session(bind=engine) as db:
        has_any = db.scalar(select(ReferralRule).limit(1))
        if has_any:
            return
        db.add_all([
            ReferralRule(level=1, share=0.70),
            ReferralRule(level=2, share=0.30),
        ])
        db.commit()

seed_referral_rules()


@app.get("/health")
def health():
    return {"ok": True}

# 라우터는 app 만든 뒤에!
app.include_router(auth_router)
app.include_router(admin_router)
