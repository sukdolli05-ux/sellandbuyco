from fastapi import FastAPI
from app.domain.auth.api import router as auth_router

app = FastAPI(
    title="SellAndBuyCo API",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth_router)
