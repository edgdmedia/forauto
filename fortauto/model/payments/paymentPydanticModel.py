from pydantic import BaseModel, Field
from typing import List, Optional
class UserPayment(BaseModel):
    services:List[dict]
    payment_status:str
    payment_RefNo:Optional[str]
    method:Optional[str] = "direct"
    total_amount:Optional[int] = 0.00

class UserDeposit(BaseModel):
    payment_RefNo:str
    total_amount:int = Field(..., min=500)

class UpdatePayment(BaseModel):
    payment_RefNo:str
    payment_status:Optional[str]
    total_amount:Optional[int]

class UpdateDeposit(BaseModel):
    userId:str
    total_amount:int
    method:Optional[str] = "credit"