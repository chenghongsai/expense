from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import relationship
from .db import mapper_registry, metadata
from .domain import User, Ticket

users_table = Table(
    "users", metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(255), unique=True, nullable=False),
    Column("password_hash", String(255), nullable=False),
    Column("role", String(10), nullable=False),  # EMPLOYEE / EMPLOYER
    Column("is_suspended", Boolean, nullable=False, server_default="false"),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

tickets_table = Table(
    "tickets", metadata,
    Column("ticket_id", Integer, primary_key=True, autoincrement=True),
    Column("owner_id", ForeignKey("users.user_id"), nullable=False),
    Column("spent_at", DateTime(timezone=True), nullable=False),
    Column("amount", Numeric(12, 2), nullable=False),
    Column("link", Text, nullable=True),
    Column("description", Text, nullable=True),
    Column("status", String(10), nullable=False, server_default="PENDING"),
    Column("is_visible", Boolean, nullable=False, server_default="true"),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

def map_model_to_tables():
    mapper_registry.map_imperatively(
        User, users_table,
        properties={
            "id": users_table.c.user_id,
            "tickets": relationship("Ticket", back_populates="owner", lazy="selectin"),
        },
    )
    mapper_registry.map_imperatively(
        Ticket, tickets_table,
        properties={
            "id": tickets_table.c.ticket_id,
            "owner": relationship("User", back_populates="tickets"),
            "owner_id": tickets_table.c.owner_id,
        },
    )
