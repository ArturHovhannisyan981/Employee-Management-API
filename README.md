# Employee Management System

## Overview

The Employee Management System is a robust RESTful API built with **FastAPI** and **PostgreSQL**, designed to streamline employee data management within an organization. It offers secure user authentication, comprehensive employee record handling, and seamless integration with PostgreSQL for reliable data storage.

## Features

- **User Authentication**: Secure user registration and login functionalities.
- **Employee Management**: Create, retrieve, update, and delete employee records.
- **Department and Position Management**: Organize employees by departments and positions.
- **Data Validation**: Utilizes Pydantic models for data validation and serialization.
- **Database Integration**: Employs SQLAlchemy for ORM and Alembic for database migrations.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python.
- **PostgreSQL**: Advanced, open-source relational database.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Alembic**: Lightweight database migration tool for SQLAlchemy.
- **Pydantic**: Data validation and settings management using Python type annotations.

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/your-username/employee-management-system.git
    cd employee-management-system
    ```

2. **Create a Virtual Environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:

    Create a `.env` file in the project root directory with the following content:

    ```ini
    DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/employee_management
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

    Replace `username`, `password`, and `your_secret_key` with your PostgreSQL credentials and a secret key for JWT tokens.

5. **Apply Database Migrations**:

    ```sh
    alembic upgrade head
    ```

6. **Run the Application**:

    ```sh
    uvicorn main:app --reload
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

- **User Authentication**:
    - `POST /register/`: Register a new user.
    - `POST /login/`: Authenticate a user and obtain a JWT token.

- **Employee Management**:
    - `POST /employees/`: Create a new employee record.
    - `GET /employees/`: Retrieve all employee records.
    - `GET /employees/{employee_id}/`: Retrieve a specific employee record by ID.
    - `PUT /employees/{employee_id}/`: Update an existing employee record.
    - `DELETE /employees/{employee_id}/`: Delete an employee record.

- **Department Management**:
    - `POST /departments/`: Create a new department.
    - `GET /departments/`: Retrieve all departments.

- **Position Management**:
    - `POST /positions/`: Create a new position.
    - `GET /positions/`: Retrieve all positions.

## Running Tests

To ensure the application functions as expected, run the test suite using `pytest`:

```sh
pytest
