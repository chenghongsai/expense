from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db, get_current_user, require_role
from ..domain import User, Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])

class TicketIn(BaseModel):
    spent_at: datetime
    amount: Decimal
    link: Optional[str] = None
    description: Optional[str] = None

class TicketOut(BaseModel):
    id: int
    owner_id: int
    spent_at: datetime
    amount: Decimal
    link: Optional[str] = None
    description: Optional[str] = None
    status: str

    @classmethod
    def from_orm_ticket(cls, t: Ticket) -> "TicketOut":
        return cls(id=t.id, owner_id=t.owner_id, spent_at=t.spent_at, amount=t.amount,
                   link=t.link, description=t.description, status=t.status)

# 员工创建自己的报销单
@router.post("", response_model=TicketOut, dependencies=[Depends(require_role("EMPLOYEE"))])
async def create_ticket(data: TicketIn, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    ticket = Ticket(owner=user, spent_at=data.spent_at, amount=data.amount,
                    link=data.link, description=data.description)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return TicketOut.from_orm_ticket(ticket)

# 员工只看自己的（且未软删）
@router.get("/me", response_model=List[TicketOut], dependencies=[Depends(require_role("EMPLOYEE"))])
async def list_my_tickets(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    res = await db.execute(select(Ticket).where(Ticket.owner_id == user.id, Ticket.is_visible == True))
    tickets = res.scalars().all()
    return [TicketOut.from_orm_ticket(t) for t in tickets]

# 雇主看所有人的（长列表，未软删）
@router.get("", response_model=List[TicketOut], dependencies=[Depends(require_role("EMPLOYER"))])
async def list_all_tickets(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Ticket).where(Ticket.is_visible == True))
    tickets = res.scalars().all()
    return [TicketOut.from_orm_ticket(t) for t in tickets]
