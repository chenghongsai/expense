from datetime import datetime
from decimal import Decimal
from typing import List, Optional

class User:
    def __init__(self, email: str, password_hash: str, role: str = "EMPLOYEE", is_suspended: bool = False):
        self.id: int | None = None
        self.email = email
        self.password_hash = password_hash
        self.role = role            # "EMPLOYEE" | "EMPLOYER"
        self.is_suspended = is_suspended
        self.created_at: datetime | None = None
        self.tickets: List["Ticket"] = []

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
        self.spent_at = spent_at
        self.amount = amount
        self.link = link
        self.description = description
        self.status = status        # "PENDING" | "APPROVED" | "DENIED"
        self.is_visible = is_visible
        self.created_at: datetime | None = None
