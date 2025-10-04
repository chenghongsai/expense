from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..domain import User
from ..security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    role: str  # "EMPLOYEE" or "EMPLOYER"

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenOut)
async def register(data: RegisterIn, db: AsyncSession = Depends(lambda: SessionLocal())):
    exists = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    await db.commit()
    return TokenOut(access_token=create_access_token(sub=user.email, extra={"role": user.role}))

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenOut)
async def login(data: LoginIn, db: AsyncSession = Depends(lambda: SessionLocal())):
    res = await db.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Bad credentials")
    if user.role == "EMPLOYEE" and user.is_suspended:
        raise HTTPException(status_code=403, detail="Suspended")
    return TokenOut(access_token=create_access_token(sub=user.email, extra={"role": user.role}))
