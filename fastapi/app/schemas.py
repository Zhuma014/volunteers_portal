from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from app.models import UserRole  



# ==== ENUMS ====

class UserRole(str, Enum):
    volunteer = "volunteer"
    antikor_staff = "antikor_staff"

class CaseStatus(str, Enum):
    submitted = "submitted"
    in_review = "in_review"
    rejected = "rejected"
    accepted = "accepted"


# ==== USER ====

class UserBase(BaseModel):
    iin: str = Field(..., min_length=12, max_length=12)
    
    phone_number: Optional[str]

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = None
    first_name: str  # обязательно
    last_name: str   # обязательно

class UserLogin(BaseModel):
    iin: str
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    role: Optional[UserRole] = None




# ==== STATEMENT ====

class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class StatementCreate(BaseModel):
    case_id: int
    organization_id: int
    content: str

class StatementResponse(BaseModel):
    id: int
    case_id: int
    organization: OrganizationResponse
    content: str
    created_at: datetime

    class Config:
        orm_mode = True



# ==== NOTIFICATION ====

class NotificationResponse(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True


# ==== FEEDBACK ====

class FeedbackCreate(BaseModel):
    message: str

class FeedbackResponse(BaseModel):
    id: int
    case_id: int
    staff_id: int
    message: str
    created_at: datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    user_id: int
    token: str
    created_at: datetime

    class Config:
        orm_mode = True

class RegionSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CitySchema(BaseModel):
    id: int
    name: str
    region_id: int

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# ==== CASE (Complaint) ====

class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    address: Optional[str] = None


class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    address: str                   
    region_id: int                
    city_id: int                   
    category_id: int            


class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    status: Optional[CaseStatus] = None
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    category_id: Optional[int] = None


class CaseResponse(CaseBase):
    id: int
    status: CaseStatus
    created_at: datetime
    updated_at: Optional[datetime]

    region: RegionSchema
    city: CitySchema
    category: CategorySchema
    owner: UserResponse
    feedbacks: List[FeedbackResponse]  

    class Config:
        orm_mode = True