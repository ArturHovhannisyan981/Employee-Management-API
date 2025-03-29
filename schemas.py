

from pydantic import BaseModel
from datetime import date





class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str



class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        orm_mode = True



class PositionBase(BaseModel):
    title: str

class PositionCreate(PositionBase):
    pass

class PositionOut(PositionBase):
    id: int

    class Config:
        orm_mode = True



class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    department_id: int
    position_id: int
    salary: float
    hire_date: date

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
