from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base import Base

class CommissionLedger(Base):
    __tablename__ = "commission_ledger"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    trader_user_id: Mapped[str] = mapped_column(String(36), index=True)     # 거래한 사람
    beneficiary_user_id: Mapped[str] = mapped_column(String(36), index=True) # 커미션 받는 사람(추천인)

    level: Mapped[int] = mapped_column(nullable=False)  # 1 or 2
    trade_amount: Mapped[float] = mapped_column(Float, nullable=False)
    fee_amount: Mapped[float] = mapped_column(Float, nullable=False)
    referral_pool_amount: Mapped[float] = mapped_column(Float, nullable=False)
    commission_amount: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
