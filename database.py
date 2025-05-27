from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models import EmployeePosition, VacationStatus, BusinessTripStatus

# SQLite database for simplicity
SQLALCHEMY_DATABASE_URL = "sqlite:///./employees.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class DBEmployee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    position = Column(SQLEnum(EmployeePosition), nullable=False)
    department = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    # Relationships
    vacations = relationship("DBVacation", back_populates="employee")
    business_trips = relationship("DBBusinessTrip", back_populates="employee")


class DBVacation(Base):
    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(500), nullable=True)
    status = Column(SQLEnum(VacationStatus), default=VacationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Relationships
    employee = relationship("DBEmployee", back_populates="vacations", foreign_keys=[employee_id])
    approver = relationship("DBEmployee", foreign_keys=[approved_by])


class DBBusinessTrip(Base):
    __tablename__ = "business_trips"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    destination = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    purpose = Column(String(500), nullable=False)
    estimated_cost = Column(Float, nullable=True)
    actual_cost = Column(Float, nullable=True)
    status = Column(SQLEnum(BusinessTripStatus), default=BusinessTripStatus.PLANNED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey("employees.id"), nullable=True)

    # Relationships
    employee = relationship("DBEmployee", back_populates="business_trips", foreign_keys=[employee_id])
    approver = relationship("DBEmployee", foreign_keys=[approved_by])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)