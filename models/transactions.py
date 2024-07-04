from models.base import Base

from sqlalchemy.sql import func
from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column
from flask_login import UserMixin

class Transactions(Base, UserMixin):
    __tablename__ = 'transactions'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    to_account_id = mapped_column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))    
    amount = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    type = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())