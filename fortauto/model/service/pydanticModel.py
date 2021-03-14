from pydantic import BaseModel, Field
from typing import Optional
class ServiceListInput(BaseModel):
    name:str = Field(max_length=30, min_length=3)
    price:int

class ServiceUpdateInput(BaseModel):
    id:str = Field(...)
    price:int
    name:str = Field(..., max_length=30, min_length=3)

class ServiceInput(BaseModel):
    car_type:str
    service_type:str
    additional_notes:Optional[str] = "No note"
    quantity:Optional[int]
    priority:Optional[str]
    date:Optional[str]

class ServiceUpdate(BaseModel):
    serviceId:str
    car_type:str
    service_type:str
    additional_notes:str
    quantity:Optional[int]
    priority:Optional[str]
    date:Optional[str]

class ServiceCategoryInput(BaseModel):
    name:str = Field(max_length=30, min_length=3)

class ServiceCategoryUpdateInput(BaseModel):
    id:str = Field(...)
    name:str = Field(..., max_length=30, min_length=3)
