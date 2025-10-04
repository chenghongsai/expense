from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import settings

_pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(p: str) -> str:
    return _pwd_ctx.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return _pwd_ctx.verify(p, hashed)

def create_access_token(sub: str, extra: dict | None = None) -> str:
    payload = {"sub": sub, "iat": datetime.now(timezone.utc)}
    if extra:
        payload.update(extra)
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
