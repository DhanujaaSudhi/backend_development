from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True) # Null until claimed
    is_active = Column(Boolean, default=False)
    role = Column(String, default="standard")
