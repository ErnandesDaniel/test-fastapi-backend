from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import (
    Employee, EmployeeCreate, EmployeeUpdate, EmployeeWithDetails,
    Vacation, VacationCreate, VacationUpdate, VacationWithEmployee, VacationStatus,
    BusinessTrip, BusinessTripCreate, BusinessTripUpdate, BusinessTripWithEmployee, BusinessTripStatus
)
import crud

app = FastAPI(
    title="Employee Management API",
    description="API для управления сотрудниками, их отпусками и командировками",
    version="1.0.0"
)

# Create database tables on startup
create_tables()


# Employee endpoints
@app.post("/employees/", response_model=Employee, tags=["employees"])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Создать нового сотрудника"""
    db_employee = crud.get_employee_by_email(db, email=employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db=db, employee=employee)


@app.get("/employees/", response_model=List[Employee], tags=["employees"])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех сотрудников"""
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees


@app.get("/employees/{employee_id}", response_model=EmployeeWithDetails, tags=["employees"])
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    """Получить информацию о сотруднике с его отпусками и командировками"""
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.put("/employees/{employee_id}", response_model=Employee, tags=["employees"])
def update_employee(employee_id: int, employee_update: EmployeeUpdate, db: Session = Depends(get_db)):
    """Обновить информацию о сотруднике"""
    db_employee = crud.update_employee(db, employee_id=employee_id, employee_update=employee_update)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.delete("/employees/{employee_id}", tags=["employees"])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Удалить сотрудника"""
    success = crud.delete_employee(db, employee_id=employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


# Vacation endpoints
@app.post("/vacations/", response_model=Vacation, tags=["vacations"])
def create_vacation(vacation: VacationCreate, db: Session = Depends(get_db)):
    """Создать заявку на отпуск"""
    # Check if employee exists
    db_employee = crud.get_employee(db, employee_id=vacation.employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Validate dates
    if vacation.start_date >= vacation.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    return crud.create_vacation(db=db, vacation=vacation)


@app.get("/vacations/", response_model=List[VacationWithEmployee], tags=["vacations"])
def read_vacations(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[VacationStatus] = Query(None, description="Filter by vacation status"),
    db: Session = Depends(get_db)
):
    """Получить список отпусков с возможностью фильтрации по статусу"""
    if status:
        vacations = crud.get_vacations_by_status(db, status=status)
    else:
        vacations = crud.get_vacations(db, skip=skip, limit=limit)
    return vacations


@app.get("/vacations/{vacation_id}", response_model=VacationWithEmployee, tags=["vacations"])
def read_vacation(vacation_id: int, db: Session = Depends(get_db)):
    """Получить информацию об отпуске"""
    db_vacation = crud.get_vacation(db, vacation_id=vacation_id)
    if db_vacation is None:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return db_vacation


@app.get("/employees/{employee_id}/vacations", response_model=List[Vacation], tags=["vacations"])
def read_employee_vacations(employee_id: int, db: Session = Depends(get_db)):
    """Получить все отпуска сотрудника"""
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.get_employee_vacations(db, employee_id=employee_id)


@app.put("/vacations/{vacation_id}", response_model=Vacation, tags=["vacations"])
def update_vacation(vacation_id: int, vacation_update: VacationUpdate, db: Session = Depends(get_db)):
    """Обновить заявку на отпуск"""
    db_vacation = crud.update_vacation(db, vacation_id=vacation_id, vacation_update=vacation_update)
    if db_vacation is None:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return db_vacation


@app.post("/vacations/{vacation_id}/approve", response_model=Vacation, tags=["vacations"])
def approve_vacation(vacation_id: int, approver_id: int, db: Session = Depends(get_db)):
    """Одобрить отпуск"""
    # Check if approver exists
    db_approver = crud.get_employee(db, employee_id=approver_id)
    if not db_approver:
        raise HTTPException(status_code=404, detail="Approver not found")
    
    db_vacation = crud.approve_vacation(db, vacation_id=vacation_id, approver_id=approver_id)
    if db_vacation is None:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return db_vacation


@app.post("/vacations/{vacation_id}/reject", response_model=Vacation, tags=["vacations"])
def reject_vacation(vacation_id: int, approver_id: int, db: Session = Depends(get_db)):
    """Отклонить отпуск"""
    # Check if approver exists
    db_approver = crud.get_employee(db, employee_id=approver_id)
    if not db_approver:
        raise HTTPException(status_code=404, detail="Approver not found")
    
    db_vacation = crud.reject_vacation(db, vacation_id=vacation_id, approver_id=approver_id)
    if db_vacation is None:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return db_vacation


@app.delete("/vacations/{vacation_id}", tags=["vacations"])
def delete_vacation(vacation_id: int, db: Session = Depends(get_db)):
    """Удалить заявку на отпуск"""
    success = crud.delete_vacation(db, vacation_id=vacation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vacation not found")
    return {"message": "Vacation deleted successfully"}


# Business Trip endpoints
@app.post("/business-trips/", response_model=BusinessTrip, tags=["business-trips"])
def create_business_trip(trip: BusinessTripCreate, db: Session = Depends(get_db)):
    """Создать заявку на командировку"""
    # Check if employee exists
    db_employee = crud.get_employee(db, employee_id=trip.employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Validate dates
    if trip.start_date >= trip.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    
    return crud.create_business_trip(db=db, trip=trip)


@app.get("/business-trips/", response_model=List[BusinessTripWithEmployee], tags=["business-trips"])
def read_business_trips(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[BusinessTripStatus] = Query(None, description="Filter by business trip status"),
    db: Session = Depends(get_db)
):
    """Получить список командировок с возможностью фильтрации по статусу"""
    if status:
        trips = crud.get_business_trips_by_status(db, status=status)
    else:
        trips = crud.get_business_trips(db, skip=skip, limit=limit)
    return trips


@app.get("/business-trips/{trip_id}", response_model=BusinessTripWithEmployee, tags=["business-trips"])
def read_business_trip(trip_id: int, db: Session = Depends(get_db)):
    """Получить информацию о командировке"""
    db_trip = crud.get_business_trip(db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Business trip not found")
    return db_trip


@app.get("/employees/{employee_id}/business-trips", response_model=List[BusinessTrip], tags=["business-trips"])
def read_employee_business_trips(employee_id: int, db: Session = Depends(get_db)):
    """Получить все командировки сотрудника"""
    db_employee = crud.get_employee(db, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.get_employee_business_trips(db, employee_id=employee_id)


@app.put("/business-trips/{trip_id}", response_model=BusinessTrip, tags=["business-trips"])
def update_business_trip(trip_id: int, trip_update: BusinessTripUpdate, db: Session = Depends(get_db)):
    """Обновить заявку на командировку"""
    db_trip = crud.update_business_trip(db, trip_id=trip_id, trip_update=trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Business trip not found")
    return db_trip


@app.post("/business-trips/{trip_id}/approve", response_model=BusinessTrip, tags=["business-trips"])
def approve_business_trip(trip_id: int, approver_id: int, db: Session = Depends(get_db)):
    """Одобрить командировку"""
    # Check if approver exists
    db_approver = crud.get_employee(db, employee_id=approver_id)
    if not db_approver:
        raise HTTPException(status_code=404, detail="Approver not found")
    
    db_trip = crud.approve_business_trip(db, trip_id=trip_id, approver_id=approver_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Business trip not found")
    return db_trip


@app.post("/business-trips/{trip_id}/complete", response_model=BusinessTrip, tags=["business-trips"])
def complete_business_trip(trip_id: int, actual_cost: Optional[float] = None, db: Session = Depends(get_db)):
    """Завершить командировку"""
    db_trip = crud.complete_business_trip(db, trip_id=trip_id, actual_cost=actual_cost)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Business trip not found or not in progress")
    return db_trip


@app.delete("/business-trips/{trip_id}", tags=["business-trips"])
def delete_business_trip(trip_id: int, db: Session = Depends(get_db)):
    """Удалить заявку на командировку"""
    success = crud.delete_business_trip(db, trip_id=trip_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business trip not found")
    return {"message": "Business trip deleted successfully"}


@app.get("/", tags=["root"])
def read_root():
    """Главная страница API"""
    return {
        "message": "Employee Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
