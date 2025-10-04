from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import SessionLocal
from .security import decode_token
from .domain import User

bearer = HTTPBearer(auto_error=True)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_token(cred.credentials)
        email = payload["sub"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # 被 suspend 的员工禁止访问
    if user.role == "EMPLOYEE" and user.is_suspended:
        raise HTTPException(status_code=403, detail="Suspended")
    return user

def require_role(role: str):
    async def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return _dep
