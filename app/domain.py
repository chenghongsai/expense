from datetime import datetime
from decimal import Decimal
from typing import List, Optional

# 领域模型（纯 Python 类，不包含 ORM 逻辑）
class User:
    def __init__(self, email: str, password_hash: str, role: str = "EMPLOYEE", is_suspended: bool = False):
        self.id: int | None = None
        self.email = email
        self.password_hash = password_hash
        self.role = role                # 用户角色：EMPLOYEE / EMPLOYER
        self.is_suspended = is_suspended # 是否被冻结
        self.created_at: datetime | None = None
        self.tickets: List["Ticket"] = []  # 用户创建的票据集合

class Ticket:
    def __init__(
        self,
        owner: User,
        spent_at: datetime,
        amount: Decimal,
        link: Optional[str] = None,
        description: Optional[str] = None,
        status: str = "PENDING",
        is_visible: bool = True,
    ):
        self.id: int | None = None
        self.owner = owner
        self.owner_id: int | None = None
        self.spent_at = spent_at            # 消费时间
        self.amount = amount                # 金额
        self.link = link                    # 相关链接（收据）
        self.description = description      # 备注说明
        self.status = status                # 审核状态：PENDING / APPROVED / DENIED
        self.is_visible = is_visible        # 是否可见（软删除）
        self.created_at: datetime | None = None
