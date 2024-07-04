from models.base import Base

from sqlalchemy.sql import func
from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Enum, UniqueConstraint
from sqlalchemy.orm import mapped_column
from flask_login import UserMixin

class Accounts(Base, UserMixin):
    __tablename__ = 'accounts'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    account_type = mapped_column(Enum('checking', 'saving', name='account_type_enum'), nullable=False)
    account_number = mapped_column(String(255), nullable=False)
    balance = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('account_number', name='accounts_unique'),
    )