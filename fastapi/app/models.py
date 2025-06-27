# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum


class UserRole(enum.Enum):
    volunteer = "volunteer"
    antikor_staff = "antikor_staff"

    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    password_hash = Column(String, nullable=True)  
    role = Column(Enum(UserRole), default=UserRole.volunteer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # связи
    complaints = relationship("Case", back_populates="owner")
    statements = relationship("Statement", back_populates="owner")
    notifications = relationship("Notification", back_populates="user")


class CaseStatus(enum.Enum):
    submitted = "submitted"
    in_review = "in_review"
    rejected = "rejected"
    accepted = "accepted"


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"))  
    city_id = Column(Integer, ForeignKey("cities.id"))     
    category_id = Column(Integer, ForeignKey("categories.id"))
    status = Column(Enum(CaseStatus), default=CaseStatus.submitted)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # связи
    owner = relationship("User", back_populates="complaints")
    statements = relationship("Statement", back_populates="case")
    feedbacks = relationship("Feedback", back_populates="case")
    region = relationship("Region")
    city = relationship("City")
    category = relationship("Category")


class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    case = relationship("Case", back_populates="statements")
    owner = relationship("User")
    organization = relationship("Organization", back_populates="statements")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    statements = relationship("Statement", back_populates="organization")



class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(512), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # связи
    user = relationship("User", back_populates="notifications")


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # сотрудник Антикор, который даёт обратную связь
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # связи
    case = relationship("Case", back_populates="feedbacks")
    staff = relationship("User")  # обратная связь от сотрудника


# Дополнительно можно создать модель для отчетов, но часто их формируют на основе запросов, 
# поэтому модели для них можно делать позже.



class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    cities = relationship("City", back_populates="region")




class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)  # ✅ Must be Integer
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="cities")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)