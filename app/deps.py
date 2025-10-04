from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import SessionLocal
from .security import decode_token
from .domain import User

bearer = HTTPBearer(auto_error=True)

# 提供数据库会话
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# 获取当前登录用户（通过 Bearer Token 解码）
async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_token(cred.credentials)   # 解码 token
        email = payload["sub"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # 员工被冻结时禁止访问
    if user.role == "EMPLOYEE" and user.is_suspended:
        raise HTTPException(status_code=403, detail="Suspended")
    return user

# 要求特定角色的依赖
def require_role(role: str):
    async def _dep(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return _dep
