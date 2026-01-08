from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.config import settings as env_settings
from app.models.settings import SettingsKV

FEE_KEY = "trade_fee_rate"

def get_trade_fee_rate(db: Session) -> float:
    row = db.scalar(select(SettingsKV).where(SettingsKV.key == FEE_KEY))
    if row and row.value_float is not None:
        return float(row.value_float)
    return float(env_settings.TRADE_FEE_RATE)
