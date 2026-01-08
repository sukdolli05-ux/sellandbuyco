from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr

from app.domain.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.domain.auth.turnstile import verify_turnstile

router = APIRouter(prefix="/auth", tags=["auth"])

# ⚠️ 임시 in-memory 유저 저장소 (다음 단계에서 DB로 교체)
_fake_users: dict[str, dict] = {}

class RegisterIn(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str
    turnstile_token: str = ""

class LoginIn(BaseModel):
    identifier: str
    password: str
    turnstile_token: str = ""

@router.post("/register")
async def register(payload: RegisterIn, req: Request):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="email or phone required")

    ok = await verify_turnstile(
        payload.turnstile_token,
        req.client.host if req.client else None,
    )
    if not ok:
        raise HTTPException(status_code=403, detail="bot verification failed")

    key = payload.email or payload.phone
    if key in _fake_users:
        raise HTTPException(status_code=409, detail="user already exists")

    _fake_users[key] = {
        "password_hash": hash_password(payload.password)
    }

    token = create_access_token(key)
    return {"access_token": token}

@router.post("/login")
async def login(payload: LoginIn, req: Request):
    ok = await verify_turnstile(
        payload.turnstile_token,
        req.client.host if req.client else None,
    )
    if not ok:
        raise HTTPException(status_code=403, detail="bot verification failed")

    user = _fake_users.get(payload.identifier)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token(payload.identifier)
    return {"access_token": token}
