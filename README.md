# Task Management Application - QA Portfolio Project

A comprehensive Quality Assurance portfolio project demonstrating various testing methodologies and best practices in software testing. This project includes a Flask-based task management application with complete test coverage including manual testing, automated UI testing, API testing, database testing, and performance testing.

## 🚀 Features

- User authentication and authorization
- Task CRUD operations (Create, Read, Update, Delete)
- RESTful API endpoints
- PostgreSQL database integration
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions

## 🛠 Technology Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Testing Frameworks**:
  - Selenium (UI Testing)
  - PyTest (Unit and Integration Testing)
  - Requests (API Testing)
  - JMeter (Performance Testing)
- **CI/CD**: GitHub Actions
- **Documentation**: Allure Reports

## 📋 Project Structure

```
task_management/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── static/
├── requirements.txt
└── README.md
```

## 🔧 Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task_management
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other configurations
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```
