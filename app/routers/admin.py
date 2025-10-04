from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db, require_role
from ..domain import Ticket, User

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role("EMPLOYER"))])

@router.post("/tickets/{ticket_id}/approve")
async def approve_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t.status = "APPROVED"
    await db.commit()
    return {"ok": True}

@router.post("/tickets/{ticket_id}/deny")
async def deny_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t.status = "DENIED"
    await db.commit()
    return {"ok": True}

# 冻结员工 + 软删除其票据
@router.post("/employees/{user_id}/suspend")
async def suspend_employee(user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.id == user_id))
    u = res.scalar_one_or_none()
    if not u or u.role != "EMPLOYEE":
        raise HTTPException(status_code=404, detail="Employee not found")
    u.is_suspended = True
    await db.execute(update(Ticket).where(Ticket.owner_id == u.id).values(is_visible=False))
    await db.commit()
    return {"ok": True}
