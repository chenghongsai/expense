from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..deps import get_db, require_role
from ..domain import Ticket, User

# 路由分组：雇主管理接口 /admin
# 注意：整个分组都强制要求雇主角色
router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_role("EMPLOYER"))])

@router.post("/tickets/{ticket_id}/approve")
async def approve_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """
    审批票据：把状态置为 APPROVED
    """
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t.status = "APPROVED"
    await db.commit()
    return {"ok": True}

@router.post("/tickets/{ticket_id}/deny")
async def deny_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """
    否决票据：把状态置为 DENIED
    """
    res = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    t.status = "DENIED"
    await db.commit()
    return {"ok": True}

@router.post("/employees/{user_id}/suspend")
async def suspend_employee(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    冻结员工：
    1) 将该用户标记为 is_suspended=True（员工将无法再登录）
    2) 将该员工所有票据 is_visible=False（软删除：列表中隐藏，但数据仍在）
    """
    res = await db.execute(select(User).where(User.id == user_id))
    u = res.scalar_one_or_none()

    if not u or u.role != "EMPLOYEE":
        # 只能冻结“员工”，且必须存在
        raise HTTPException(status_code=404, detail="Employee not found")

    # 冻结员工
    u.is_suspended = True

    # 软删除该员工的所有票据
    await db.execute(update(Ticket).where(Ticket.owner_id == u.id).values(is_visible=False))

    await db.commit()
    return {"ok": True}
