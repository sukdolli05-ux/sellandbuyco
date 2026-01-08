from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
import uuid

from app.db.session import get_db
from app.core.config import settings as env
from app.models.user import User
from app.models.referral import ReferralRule
from app.models.commission import CommissionLedger

router = APIRouter(prefix="/trade", tags=["trade"])

class SimTradeIn(BaseModel):
    trader_email: str
    amount: float

@router.post("/simulate")
def simulate_trade(payload: SimTradeIn, db: Session = Depends(get_db)):
    trader = db.scalar(select(User).where(User.email == payload.trader_email))
    if not trader:
        raise HTTPException(404, "trader not found")
    if payload.amount <= 0:
        raise HTTPException(400, "amount must be > 0")

    fee = payload.amount * float(env.TRADE_FEE_RATE)
    pool = fee * float(env.REFERRAL_POOL_RATE)

    # rules (L1/L2)
    rules = db.scalars(select(ReferralRule).order_by(ReferralRule.level.asc())).all()
    rule_map = {r.level: float(r.share) for r in rules}
    l1_share = rule_map.get(1, 0.70)
    l2_share = rule_map.get(2, 0.30)

    # 추천인 체인: trader.referred_by (L1) -> 그 사람의 referred_by (L2)
    commissions = []
    l1 = db.get(User, trader.referred_by) if trader.referred_by else None
    l2 = db.get(User, l1.referred_by) if (l1 and l1.referred_by) else None

    if l1:
        commissions.append(("L1", l1, pool * l1_share, 1))
    if l2:
        commissions.append(("L2", l2, pool * l2_share, 2))

    # ledger 기록
    for _, beneficiary, amount, level in commissions:
        row = CommissionLedger(
            id=str(uuid.uuid4()),
            trader_user_id=trader.id,
            beneficiary_user_id=beneficiary.id,
            level=level,
            trade_amount=float(payload.amount),
            fee_amount=float(fee),
            referral_pool_amount=float(pool),
            commission_amount=float(amount),
        )
        db.add(row)

    db.commit()

    return {
        "trade_amount": payload.amount,
        "fee_rate": float(env.TRADE_FEE_RATE),
        "fee_amount": fee,
        "referral_pool_rate": float(env.REFERRAL_POOL_RATE),
        "referral_pool_amount": pool,
        "payouts": [
            {"level": lvl, "beneficiary_email": u.email, "amount": amt}
            for (lvl, u, amt, _leveln) in commissions
        ],
    }
