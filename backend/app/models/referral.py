from sqlalchemy import Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ReferralRule(Base):
    __tablename__ = "referral_rules"

    level: Mapped[int] = mapped_column(Integer, primary_key=True)  # 1,2
    share: Mapped[float] = mapped_column(Float, nullable=False)    # ex) 0.70, 0.30
