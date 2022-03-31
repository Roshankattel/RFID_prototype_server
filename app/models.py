from enum import unique
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    amount = Column(Integer,nullable=False,unique= False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=False)
    tag_data = Column(String, nullable=False, unique=True)   #data stored in tag
    amount = Column(Integer, nullable=False, unique=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Integer, nullable=False, unique=False)
    recharge_request = Column(Boolean,nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    merchant_id = Column(Integer, ForeignKey(
        "merchants.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

    