#   Task Management API
### Description

This application is a REST API for task management with the ability to log completed tasks. The API is developed using FastAPI and includes the following features:

CRUD operations for tasks (TaskItem) and completed task records (TaskRecord).

User authentication using JWT tokens.

Authorization to ensure that users can only manage their own completed task records.
    
### Technologies and Libraries

***FastAPI*** — A high-performance web framework for building APIs with Python.

***SQLAlchemy*** — A library for working with databases, used here to define data models.

***Pydantic*** — A library for data validation and serialization.

***JWT*** — A technology for authentication and authorization using tokens.

***PostgreSQL/MySQL/SQLite*** — The database used can be any of these.


### Main Entities and Their Purpose
#### TaskItem (Task)

This is the primary entity representing a task that needs to be completed. The task model includes:

    title (name)
    description (description)
    priority (priority: low, medium, high)
    due_date (deadline)

#### TaskRecord (Completed Task Record)

This entity represents a record of a completed task. The model includes:

    user_id (reference to the user who completed the task)
    task_id (reference to the task)
    completion_date (date when the task was completed)
    time_spent (time spent on the task in minutes)

#### User

This entity represents a user in the system. It includes:

    email (email address)
    username (username)
    hashed_password (hashed password for secure storage)
    is_active, is_superuser, is_verified (flags for user status)

### API Endpoints
1. TaskRecordItem CRUD

Endpoints for working with tasks:

    POST /api/user_task/ — create a task.
    GET /api/user_tasks/ — retrieve tasks.
    PUT /api/user_task/{id} — update a task.
    PUT /api/user_taskrecord/{id} — update a task with record.
    DELETE /api/user_task/{id} — delete a task.

2. Authentication and Authorization

    JWT authentication is implemented using tokens.
    Users can only manage their own completed task records (permissions are enforced).

### Project Structure

    src/api/models.py — contains data models (User, TaskItem, TaskRecord) defined using SQLAlchemy.
    src/api/schemas.py — contains Pydantic schemas for data validation and serialization.
    src/api/task_item.py — implementation of CRUD operations for TaskRecordItem.
    src/main.py — entry point of the application where routes (endpoints) are registered and the application is configured.

### Installation and Setup

To run the project, ensure you have:

    Python 3.8 or higher
    PostgreSQL or any supported database (SQLite, MySQL)
    pip (Python package manager)

Clone the repository:

    git clone https://github.com/your_username/task-management-api.git
    cd task-management-api

Install the dependencies:

    pip install -r requirements.txt

Apply the migrations to create the database tables:

    alembic upgrade head

Running the Application

Start the development server using Uvicorn:

    uvicorn src.main:app --reload

### Conclusion

This API is designed for task management and monitoring task completion. It implements a modern security approach using JWT tokens and supports flexible data operations through a REST API. The built-in analytics features allow users to track their progress and time spent on tasks.
