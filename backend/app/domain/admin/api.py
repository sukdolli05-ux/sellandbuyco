from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from sqlalchemy import select
from app.models.settings import SettingsKV

router = APIRouter(prefix="/admin", tags=["admin"])

class FeeUpdateIn(BaseModel):
    fee_rate: float  # 0.20 means 20%

@router.get("/fee")
def get_fee(db: Session = Depends(get_db)):
    row = db.scalar(select(SettingsKV).where(SettingsKV.key == "trade_fee_rate"))
    return {"fee_rate": row.value_float if row and row.value_float is not None else None}

@router.post("/fee")
def set_fee(payload: FeeUpdateIn, db: Session = Depends(get_db)):
    if payload.fee_rate < 0 or payload.fee_rate > 1:
        raise HTTPException(400, "fee_rate must be between 0 and 1")

    row = db.get(SettingsKV, "trade_fee_rate")
    if not row:
        row = SettingsKV(key="trade_fee_rate", value_float=payload.fee_rate)
        db.add(row)
    else:
        row.value_float = payload.fee_rate

    db.commit()
    return {"ok": True, "fee_rate": payload.fee_rate}
