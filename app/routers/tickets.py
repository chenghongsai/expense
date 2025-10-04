from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db, get_current_user, require_role
from ..domain import User, Ticket

# 路由分组：票据相关接口 /tickets
router = APIRouter(prefix="/tickets", tags=["tickets"])

# --------- 请求/响应模型 ---------

class TicketIn(BaseModel):
    """
    创建票据请求体
    who（谁）不让前端传，后端用当前登录用户自动绑定为 owner
    """
    spent_at: datetime            # 什么时候消费
    amount: Decimal               # 金额
    link: Optional[str] = None    # 相关凭证链接
    description: Optional[str] = None  # 备注

class TicketOut(BaseModel):
    """
    票据返回体（给前端的安全字段）
    """
    id: int
    owner_id: int
    spent_at: datetime
    amount: Decimal
    link: Optional[str] = None
    description: Optional[str] = None
    status: str

    @classmethod
    def from_orm_ticket(cls, t: Ticket) -> "TicketOut":
        """把 ORM 实体转成响应模型（避免直接把 ORM 对象暴露出去）"""
        return cls(
            id=t.id,
            owner_id=t.owner_id,
            spent_at=t.spent_at,
            amount=t.amount,
            link=t.link,
            description=t.description,
            status=t.status,
        )

# --------- 接口实现 ---------

@router.post(
    "",
    response_model=TicketOut,
    dependencies=[Depends(require_role("EMPLOYEE"))],  # 只有员工能创建
)
async def create_ticket(
    data: TicketIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    员工创建自己的报销单：
    - owner 自动指向当前登录用户，防止伪造
    """
    ticket = Ticket(
        owner=user,
        spent_at=data.spent_at,
        amount=data.amount,
        link=data.link,
        description=data.description,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)  # 刷新以获取数据库生成的主键等

    return TicketOut.from_orm_ticket(ticket)

@router.get(
    "/me",
    response_model=List[TicketOut],
    dependencies=[Depends(require_role("EMPLOYEE"))],  # 只有员工能访问“我的票据”
)
async def list_my_tickets(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    员工只看自己的票据，并且仅限 is_visible=True（软删除后对任何人隐藏）
    """
    res = await db.execute(
        select(Ticket).where(Ticket.owner_id == user.id, Ticket.is_visible == True)  # noqa: E712
    )
    tickets = res.scalars().all()
    return [TicketOut.from_orm_ticket(t) for t in tickets]

@router.get(
    "",
    response_model=List[TicketOut],
    dependencies=[Depends(require_role("EMPLOYER"))],  # 只有雇主能看全量列表
)
async def list_all_tickets(db: AsyncSession = Depends(get_db)):
    """
    雇主查看所有员工的票据（长列表），同样只显示 is_visible=True 的
    """
    res = await db.execute(select(Ticket).where(Ticket.is_visible == True))  # noqa: E712
    tickets = res.scalars().all()
    return [TicketOut.from_orm_ticket(t) for t in tickets]
