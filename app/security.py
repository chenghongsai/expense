from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from .config import settings

# 配置密码加密方式（bcrypt）
_pwd_ctx = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],  # 同时支持两种算法
    deprecated="auto"
)

# 对明文密码进行哈希
def hash_password(p: str) -> str:
    return _pwd_ctx.hash(p)

# 校验明文密码和哈希是否匹配
def verify_password(p: str, hashed: str) -> bool:
    return _pwd_ctx.verify(p, hashed)

# 创建 JWT Token
def create_access_token(sub: str, extra: dict | None = None) -> str:
    payload = {"sub": sub, "iat": datetime.now(timezone.utc)}  # sub = 用户标识
    if extra:
        payload.update(extra)  # 附加角色等信息
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

# 解码 JWT Token
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
