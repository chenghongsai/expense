from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..domain import User
from ..security import hash_password, verify_password, create_access_token

# 路由分组：所有认证相关接口都挂在 /auth 前缀下
router = APIRouter(prefix="/auth", tags=["auth"])

# --------- 请求/响应模型 ---------

class RegisterIn(BaseModel):
    """
    注册请求体：
    - email：邮箱（EmailStr 会做基本格式校验）
    - password：明文密码（服务端会哈希后存库）
    - role：角色，"EMPLOYEE" 或 "EMPLOYER"
    """
    email: EmailStr
    password: str
    role: str  # "EMPLOYEE" or "EMPLOYER"

class TokenOut(BaseModel):
    """
    登录/注册成功后统一返回 JWT：
    - access_token：实际的 token 字符串
    - token_type：规范写法 'bearer'
    """
    access_token: str
    token_type: str = "bearer"

# --------- 接口实现 ---------

@router.post("/register", response_model=TokenOut)
async def register(
    data: RegisterIn,
    db: AsyncSession = Depends(lambda: SessionLocal()),  # 这里直接临时创建一个会话
):
    """
    注册：
    1) 检查邮箱是否已存在
    2) 生成密码哈希并创建用户
    3) 提交事务
    4) 直接返回一个可用的 JWT（方便新用户无需再手动登录）
    """
    exists = (await db.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=data.email, password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    await db.commit()

    return TokenOut(access_token=create_access_token(sub=user.email, extra={"role": user.role}))

class LoginIn(BaseModel):
    """登录请求体"""
    email: EmailStr
    password: str

@router.post("/login", response_model=TokenOut)
async def login(
    data: LoginIn,
    db: AsyncSession = Depends(lambda: SessionLocal()),
):
    """
    登录：
    1) 按邮箱查用户
    2) 校验密码
    3) 如果是已冻结的员工，则禁止登录（403）
    4) 返回 JWT
    """
    res = await db.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        # 邮箱不存在或密码不匹配
        raise HTTPException(status_code=401, detail="Bad credentials")

    if user.role == "EMPLOYEE" and user.is_suspended:
        # 冻结员工禁止登录（题目要求）
        raise HTTPException(status_code=403, detail="Suspended")

    return TokenOut(access_token=create_access_token(sub=user.email, extra={"role": user.role}))
