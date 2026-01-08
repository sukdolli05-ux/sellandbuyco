import os

class Settings:
    # Auth / Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_EXPIRE_MIN: int = int(os.getenv("JWT_EXPIRE_MIN", "60"))

    # Cloudflare Turnstile
    TURNSTILE_SITE_KEY: str = os.getenv("TURNSTILE_SITE_KEY", "")
    TURNSTILE_SECRET_KEY: str = os.getenv("TURNSTILE_SECRET_KEY", "")

    # Database (dev default)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

settings = Settings()
