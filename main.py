

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger

import database, schemas, auth, crud

# Запуск логирования
logger.add("logs/app.log", rotation="1 MB", level="INFO")

# Инициализация FastAPI
app = FastAPI(title="Employee Management API")

# OAuth2 схема для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------- Регистрация и логин ----------

@app.post("/register/")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return auth.register_user(user, db)

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- Эндпоинты для сотрудников ----------

@app.get("/employees/")
def get_all_employees(db: Session = Depends(database.get_db)):
    return crud.get_employees(db)

@app.post("/employees/")
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    return crud.create_employee(db, employee)

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(database.get_db)):
    deleted_employee = crud.delete_employee(db, employee_id)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


# ---------- Эндпоинты для департаментов ----------

@app.get("/departments/")
def get_departments(db: Session = Depends(database.get_db)):
    return crud.get_departments(db)

@app.post("/departments/")
def add_department(department: schemas.DepartmentCreate, db: Session = Depends(database.get_db)):
    return crud.create_department(db, department)


# ---------- Эндпоинты для позиций ----------

@app.get("/positions/")
def get_positions(db: Session = Depends(database.get_db)):
    return crud.get_positions(db)

@app.post("/positions/")
def add_position(position: schemas.PositionCreate, db: Session = Depends(database.get_db)):
    return crud.create_position(db, position)


# ---------- Главная страница ----------

@app.get("/")
def root():
    return {"message": "Welcome to Employee Management System"}
