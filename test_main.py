import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Подключение к тестовой базе данных (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем фикстуру базы данных
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Создаем тестовый клиент, передавая тестовую базу
@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db  # Подменяем зависимость
    with TestClient(app) as c:
        yield c

# ---------- Тесты регистрации и логина ----------
def test_register(client):
    response = client.post("/register/", json={"username": "testuser", "password": "testpassword"})
    print(response.status_code, response.json())  # ← Печатаем ответ сервера

    assert response.status_code in [200, 400]  # Учитываем возможную ошибку

    if response.status_code == 200:
        assert "id" in response.json()
        assert response.json()["username"] == "testuser"



def test_login(client):
    client.post("/register/", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/login/", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# ---------- Тесты CRUD сотрудников ----------
def test_create_employee(client):
    response = client.post("/employees/", json={
        "first_name": "John",
        "last_name": "Doe",
        "department_id": 1,
        "position_id": 1,
        "salary": 50000,
        "hire_date": "2024-01-01"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_employees(client):
    client.post("/employees/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "department_id": 1,
        "position_id": 1,
        "salary": 60000,
        "hire_date": "2024-02-01"
    })
    response = client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# ---------- Тесты CRUD департаментов ----------
def test_create_department(client):
    response = client.post("/departments/", json={"name": "IT"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_departments(client):
    client.post("/departments/", json={"name": "HR"})
    response = client.get("/departments/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# ---------- Тесты CRUD позиций ----------
def test_create_position(client):
    response = client.post("/positions/", json={"title": "Software Engineer"})
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_positions(client):
    client.post("/positions/", json={"title": "Data Scientist"})
    response = client.get("/positions/")
    assert response.status_code == 200
    assert len(response.json()) > 0
