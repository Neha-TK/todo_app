# FastAPI Todo App

A simple Todo app using FastAPI and PostgreSQL with JWT authentication.

## Features

- User Signup & Login (JWT based)
- Create Todos with deadline
- Grouped Todo view:
  - Completed
  - Pending
  - Time elapsed
- Edit, Mark Complete, Delete Todo
- PostgreSQL database

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Auth
- Pydantic

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/todo_app.git
cd todo_app.git
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
Create a .env file in the root of the project and add the following environment variables:

```bash
DATABASE_URL=postgresql://your_user:your_password@localhost/todo_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

* Replace `your_user` and `your_password` with your PostgreSQL username and password.

* Set your own `SECRET_KEY` for JWT encryption.

* Adjust `ACCESS_TOKEN_EXPIRE_MINUTES` to control how long the JWT remains valid.

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

### 5. Visit

http://127.0.0.1:8000/docs
