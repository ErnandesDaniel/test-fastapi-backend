from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class EmployeePosition(str, Enum):
    DEVELOPER = "developer"
    MANAGER = "manager"
    ANALYST = "analyst"
    DESIGNER = "designer"
    QA = "qa"
    HR = "hr"
    ADMIN = "admin"


class VacationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class BusinessTripStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Employee models
class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    position: EmployeePosition
    department: str = Field(..., min_length=1, max_length=100)
    hire_date: date
    salary: Optional[float] = Field(None, ge=0)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, pattern=r'^[^@]+@[^@]+\.[^@]+$')
    position: Optional[EmployeePosition] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = Field(None, ge=0)


class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Vacation models
class VacationBase(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = Field(None, max_length=500)


class VacationCreate(VacationBase):
    pass


class VacationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = Field(None, max_length=500)
    status: Optional[VacationStatus] = None


class Vacation(VacationBase):
    id: int
    status: VacationStatus = VacationStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None
    approved_by: Optional[int] = None

    class Config:
        from_attributes = True


# Business Trip models
class BusinessTripBase(BaseModel):
    employee_id: int
    destination: str = Field(..., min_length=1, max_length=200)
    start_date: date
    end_date: date
    purpose: str = Field(..., min_length=1, max_length=500)
    estimated_cost: Optional[float] = Field(None, ge=0)


class BusinessTripCreate(BusinessTripBase):
    pass


class BusinessTripUpdate(BaseModel):
    destination: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    purpose: Optional[str] = Field(None, min_length=1, max_length=500)
    estimated_cost: Optional[float] = Field(None, ge=0)
    actual_cost: Optional[float] = Field(None, ge=0)
    status: Optional[BusinessTripStatus] = None


class BusinessTrip(BusinessTripBase):
    id: int
    status: BusinessTripStatus = BusinessTripStatus.PLANNED
    actual_cost: Optional[float] = Field(None, ge=0)
    created_at: datetime
    updated_at: Optional[datetime] = None
    approved_by: Optional[int] = None

    class Config:
        from_attributes = True


# Response models
class EmployeeWithDetails(Employee):
    vacations: List[Vacation] = []
    business_trips: List[BusinessTrip] = []


class VacationWithEmployee(Vacation):
    employee: Employee


class BusinessTripWithEmployee(BusinessTrip):
    employee: Employee