from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import DBEmployee, DBVacation, DBBusinessTrip
from models import (
    EmployeeCreate, EmployeeUpdate,
    VacationCreate, VacationUpdate,
    BusinessTripCreate, BusinessTripUpdate,
    VacationStatus, BusinessTripStatus
)


# Employee CRUD operations
def get_employee(db: Session, employee_id: int) -> Optional[DBEmployee]:
    return db.query(DBEmployee).filter(DBEmployee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[DBEmployee]:
    return db.query(DBEmployee).filter(DBEmployee.email == email).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100) -> List[DBEmployee]:
    return db.query(DBEmployee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate) -> DBEmployee:
    db_employee = DBEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee_update: EmployeeUpdate) -> Optional[DBEmployee]:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        update_data = employee_update.dict(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(db_employee, field, value)
            db.commit()
            db.refresh(db_employee)
    return db_employee


def delete_employee(db: Session, employee_id: int) -> bool:
    db_employee = get_employee(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
        return True
    return False


# Vacation CRUD operations
def get_vacation(db: Session, vacation_id: int) -> Optional[DBVacation]:
    return db.query(DBVacation).filter(DBVacation.id == vacation_id).first()


def get_vacations(db: Session, skip: int = 0, limit: int = 100) -> List[DBVacation]:
    return db.query(DBVacation).offset(skip).limit(limit).all()


def get_employee_vacations(db: Session, employee_id: int) -> List[DBVacation]:
    return db.query(DBVacation).filter(DBVacation.employee_id == employee_id).all()


def get_vacations_by_status(db: Session, status: VacationStatus) -> List[DBVacation]:
    return db.query(DBVacation).filter(DBVacation.status == status).all()


def create_vacation(db: Session, vacation: VacationCreate) -> DBVacation:
    db_vacation = DBVacation(**vacation.dict())
    db.add(db_vacation)
    db.commit()
    db.refresh(db_vacation)
    return db_vacation


def update_vacation(db: Session, vacation_id: int, vacation_update: VacationUpdate) -> Optional[DBVacation]:
    db_vacation = get_vacation(db, vacation_id)
    if db_vacation:
        update_data = vacation_update.dict(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(db_vacation, field, value)
            db.commit()
            db.refresh(db_vacation)
    return db_vacation


def approve_vacation(db: Session, vacation_id: int, approver_id: int) -> Optional[DBVacation]:
    db_vacation = get_vacation(db, vacation_id)
    if db_vacation:
        db_vacation.status = VacationStatus.APPROVED
        db_vacation.approved_by = approver_id
        db_vacation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_vacation)
    return db_vacation


def reject_vacation(db: Session, vacation_id: int, approver_id: int) -> Optional[DBVacation]:
    db_vacation = get_vacation(db, vacation_id)
    if db_vacation:
        db_vacation.status = VacationStatus.REJECTED
        db_vacation.approved_by = approver_id
        db_vacation.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_vacation)
    return db_vacation


def delete_vacation(db: Session, vacation_id: int) -> bool:
    db_vacation = get_vacation(db, vacation_id)
    if db_vacation:
        db.delete(db_vacation)
        db.commit()
        return True
    return False


# Business Trip CRUD operations
def get_business_trip(db: Session, trip_id: int) -> Optional[DBBusinessTrip]:
    return db.query(DBBusinessTrip).filter(DBBusinessTrip.id == trip_id).first()


def get_business_trips(db: Session, skip: int = 0, limit: int = 100) -> List[DBBusinessTrip]:
    return db.query(DBBusinessTrip).offset(skip).limit(limit).all()


def get_employee_business_trips(db: Session, employee_id: int) -> List[DBBusinessTrip]:
    return db.query(DBBusinessTrip).filter(DBBusinessTrip.employee_id == employee_id).all()


def get_business_trips_by_status(db: Session, status: BusinessTripStatus) -> List[DBBusinessTrip]:
    return db.query(DBBusinessTrip).filter(DBBusinessTrip.status == status).all()


def create_business_trip(db: Session, trip: BusinessTripCreate) -> DBBusinessTrip:
    db_trip = DBBusinessTrip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def update_business_trip(db: Session, trip_id: int, trip_update: BusinessTripUpdate) -> Optional[DBBusinessTrip]:
    db_trip = get_business_trip(db, trip_id)
    if db_trip:
        update_data = trip_update.dict(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            for field, value in update_data.items():
                setattr(db_trip, field, value)
            db.commit()
            db.refresh(db_trip)
    return db_trip


def approve_business_trip(db: Session, trip_id: int, approver_id: int) -> Optional[DBBusinessTrip]:
    db_trip = get_business_trip(db, trip_id)
    if db_trip and db_trip.status == BusinessTripStatus.PLANNED:
        db_trip.status = BusinessTripStatus.IN_PROGRESS
        db_trip.approved_by = approver_id
        db_trip.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_trip)
    return db_trip


def complete_business_trip(db: Session, trip_id: int, actual_cost: Optional[float] = None) -> Optional[DBBusinessTrip]:
    db_trip = get_business_trip(db, trip_id)
    if db_trip and db_trip.status == BusinessTripStatus.IN_PROGRESS:
        db_trip.status = BusinessTripStatus.COMPLETED
        if actual_cost is not None:
            db_trip.actual_cost = actual_cost
        db_trip.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_trip)
    return db_trip


def delete_business_trip(db: Session, trip_id: int) -> bool:
    db_trip = get_business_trip(db, trip_id)
    if db_trip:
        db.delete(db_trip)
        db.commit()
        return True
    return False