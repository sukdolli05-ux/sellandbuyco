import httpx
from app.core.config import settings

async def verify_turnstile(token: str, remote_ip: str | None = None) -> bool:
    # DEV mode: 키가 없으면 통과
    if not settings.TURNSTILE_SECRET_KEY:
        return True

    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        data["remoteip"] = remote_ip

    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=data,
        )
        return bool(r.json().get("success"))
