from datetime import datetime
from enum import unique
from pickle import FALSE
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

class MerchantCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    amount:int

class MerchantLogin(BaseModel):
    email:EmailStr
    password:str

class UserCreate(BaseModel):
    name:str
    tag_data:str
    amount:int

class TransactionCreate(BaseModel):
    tag_data:str
    amount:int
    recharge_request: Optional[bool] = False

class TokenData(BaseModel):
    id: Optional[str] = None

# This is for response model
class MerchantResponse(BaseModel):
    id: int
    name:str
    email: EmailStr
    amount:int
    created_at: datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):

    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    name:str
    amount:int
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    id:int 
    created_at: datetime
    user_id: int
    merchant_id : int
    amount : int

    class Config:
        orm_mode = True
