import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_EXPIRE_MIN: int = int(os.getenv("JWT_EXPIRE_MIN", "60"))

    # fee
    TRADE_FEE_RATE: float = float(os.getenv("TRADE_FEE_RATE", "0.002"))  # 0.2%
    REFERRAL_POOL_RATE: float = float(os.getenv("REFERRAL_POOL_RATE", "0.20"))  # fee의 20%

    # db
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:////workspaces/sellandbuyco/backend/dev.db",
    )

settings = Settings()
TRADE_FEE_RATE: float = float(os.getenv("TRADE_FEE_RATE", "0.002"))  # ✅ 기본 0.2%
REFERRAL_POOL_RATE: float = float(os.getenv("REFERRAL_POOL_RATE", "0.20"))  # ✅ 수수료의 20%


