from fastapi import FastAPI

from app.domain.auth.api import router as auth_router
from app.domain.admin.api import router as admin_router

from app.db.session import engine
from app.db.base import Base
from app.models import user, settings  # noqa: F401  (테이블 등록용)

app = FastAPI(title="SellAndBuyCo API", version="0.1.0")

# DB 테이블 생성 (MVP)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

# 라우터는 app 만든 뒤에!
app.include_router(auth_router)
app.include_router(admin_router)
