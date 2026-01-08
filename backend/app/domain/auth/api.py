from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid

from app.db.session import get_db
from app.models.user import User, gen_ref_code
from app.domain.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.domain.auth.turnstile import verify_turnstile

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    password: str
    turnstile_token: str = ""
    ref: str | None = None  # ✅ 추천인 코드 (선택)

class LoginIn(BaseModel):
    identifier: str  # email or phone
    password: str
    turnstile_token: str = ""

@router.post("/register")
async def register(payload: RegisterIn, req: Request, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="email or phone required")

    ok = await verify_turnstile(
        payload.turnstile_token,
        req.client.host if req.client else None,
    )
    if not ok:
        raise HTTPException(status_code=403, detail="bot verification failed")

    # 중복 체크
    if payload.email:
        exists = db.scalar(select(User).where(User.email == payload.email))
        if exists:
            raise HTTPException(status_code=409, detail="email already exists")
    if payload.phone:
        exists = db.scalar(select(User).where(User.phone == payload.phone))
        if exists:
            raise HTTPException(status_code=409, detail="phone already exists")

    # 추천인(ref) 처리 (있으면 referrer 찾기)
    referred_by = None
    if payload.ref:
        ref_user = db.scalar(select(User).where(User.referral_code == payload.ref))
        if not ref_user:
            raise HTTPException(status_code=400, detail="invalid referral code")
        referred_by = ref_user.id

    # 내 referral_code 생성 (중복 나면 재시도)
    code = gen_ref_code()
    while db.scalar(select(User).where(User.referral_code == code)):
        code = gen_ref_code()

    user = User(
        id=str(uuid.uuid4()),
        email=str(payload.email) if payload.email else None,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        referral_code=code,
        referred_by=referred_by,
    )

    db.add(user)
    db.commit()

    token = create_access_token(user.id)
    return {"access_token": token, "referral_code": user.referral_code}

@router.post("/login")
async def login(payload: LoginIn, req: Request, db: Session = Depends(get_db)):
    ok = await verify_turnstile(
        payload.turnstile_token,
        req.client.host if req.client else None,
    )
    if not ok:
        raise HTTPException(status_code=403, detail="bot verification failed")

    # identifier로 email/phone 둘 다 조회
    user = db.scalar(select(User).where(User.email == payload.identifier))
    if not user:
        user = db.scalar(select(User).where(User.phone == payload.identifier))

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token, "user_id": user.id, "referral_code": user.referral_code}
