# Expense Tracking System

A full-stack expense tracking application built with **Python, FastAPI,
Streamlit, and MySQL**. The application allows users to add and update
daily expenses and analyze spending over a selected date range with
category-wise totals and percentages.

## Features

-   Add and update expenses for a selected date
-   Store expense amount, category, and notes
-   Retrieve expenses for a specific date
-   Validate expense entries before saving
-   Category-wise expense analytics
-   Select a start date and end date for analysis
-   Calculate total spending by category
-   Calculate each category's percentage of total spending
-   Display analytics using a Streamlit bar chart
-   Display analytics in a tabular format
-   FastAPI backend for REST API endpoints
-   MySQL database for persistent storage
-   Logging for database operations
-   Pytest-based backend/database tests

## Tech Stack

  Technology               Purpose
  ------------------------ ----------------------------------------
  Python                   Application development
  FastAPI                  Backend REST API
  Streamlit                Frontend/UI
  MySQL                    Database
  Pydantic                 API request/response data models
  Pandas                   Analytics data preparation
  Requests                 Frontend-to-backend HTTP communication
  Pytest                   Testing
  Uvicorn                  FastAPI server
  mysql-connector-python   MySQL connectivity
  python-dotenv            Environment variable management

## Project Architecture

``` text
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    │      frontend/      │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    │      backend/       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    db_helper.py     │
                    │ Database operations │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       MySQL         │
                    │  expense_manager    │
                    └─────────────────────┘
```

## Project Structure

``` text
Expense Tracking Project/
│
├── backend/
│   ├── db_helper.py
│   ├── logging_setup.py
│   └── server.py
│
├── database/
│   └── expense_db_creation.sql
│
├── frontend/
│   ├── add_update_ui.py
│   ├── analytics_ui.py
│   └── app.py
│
├── tests/
│   ├── backend/
│   │   └── test_db_helper.py
│   └── conftest.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

> `server.log` is generated at runtime and is excluded from Git using
> `.gitignore`.

## How It Works

### 1. Add / Update Expenses

The **Add/Update** tab lets the user select a date and view the expenses
already stored for that date.

Each expense contains:

-   Amount
-   Category
-   Notes

Available categories in the UI are:

``` text
None
Rent
Food
Shopping
Entertainment
Other
```

The frontend sends the selected date to the FastAPI backend. Existing
expenses for that date are retrieved and displayed.

When the user submits the form, entries with a positive amount must have
a valid category. Empty/default entries are filtered out before being
sent to the backend.

### 2. Backend Expense Update

The backend exposes:

``` text
POST /expenses/{expense_date}
```

The endpoint receives a list of expenses for a date. The current
implementation removes the existing expenses for that date and then
inserts the submitted expenses.

This makes the submitted list the complete set of expenses for that
selected date.

### 3. Expense Analytics

The **Analytics** tab allows the user to select a start date and end
date.

The frontend sends the date range to:

``` text
POST /analytics/
```

The backend queries the database using a date range and groups the
results by category.

For every category, the backend calculates:

``` text
percentage = category_total / overall_total × 100
```

The frontend then displays category-wise expense totals in a bar chart
and table with category, total, and percentage.

## API Endpoints

### Get Expenses for a Date

``` http
GET /expenses/{expense_date}
```

Example:

``` text
GET /expenses/2026-08-01
```

Returns the expenses associated with the selected date.

### Add / Update Expenses

``` http
POST /expenses/{expense_date}
```

Example:

``` text
POST /expenses/2026-08-01
```

Request body:

``` json
[
  {
    "amount": 500,
    "category": "Food",
    "notes": "Groceries"
  },
  {
    "amount": 1200,
    "category": "Rent",
    "notes": "Monthly rent payment"
  }
]
```

### Get Analytics

``` http
POST /analytics/
```

Request body:

``` json
{
  "start_date": "2026-08-01",
  "end_date": "2026-08-05"
}
```

The response contains category-wise totals and percentages.

Example structure:

``` json
{
  "Rent": {
    "total": 2500,
    "percentage": 55.68
  },
  "Food": {
    "total": 1200,
    "percentage": 26.75
  }
}
```

## Database

The application uses a MySQL database named:

``` text
expense_manager
```

The SQL setup is provided in:

``` text
database/expense_db_creation.sql
```

The database helper uses MySQL Connector/Python for:

-   Fetching expenses for a date
-   Inserting expenses
-   Deleting expenses for a date
-   Fetching category-wise expense summaries

The database layer uses parameterized SQL queries for values supplied to
the queries.

## Database Configuration

Database credentials are kept outside the source code using environment
variables.

Create a `.env` file in the project root:

``` env
MYSQL_PASSWORD=your_mysql_password
```

The application uses:

``` text
Host: localhost
User: root
Database: expense_manager
```

The `.env` file is excluded from Git using `.gitignore` and should
**never be committed to GitHub**.

## Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/kshitish13/Expense-Management-Project
cd Expense-Management-Project
```

### 2. Create a Virtual Environment

Windows:

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

## Database Setup

1.  Make sure MySQL Server is installed and running.
2.  Open `database/expense_db_creation.sql`.
3.  Execute the SQL script in MySQL.
4.  Confirm that the `expense_manager` database and required tables have
    been created.
5.  Create the `.env` file in the project root and add your MySQL
    password.

## Running the Application

The project has two parts that need to run:

-   FastAPI backend
-   Streamlit frontend

### Start the FastAPI Backend

From the project root:

``` bash
uvicorn backend.server:app --reload
```

The backend will normally be available at:

``` text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

``` text
http://127.0.0.1:8000/docs
```

### Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and run:

``` bash
streamlit run frontend/app.py
```

The Streamlit application will open in your browser.

## Testing

The project uses **Pytest** for testing the database helper
functionality.

Run:

``` bash
pytest
```

The current tests cover scenarios including:

-   Fetching expenses for a valid date
-   Verifying returned expense values
-   Fetching expenses for a date with no records
-   Fetching analytics data for a date range with no records

Example test:

``` python
def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2026-08-15")

    assert len(expenses) == 1
    assert expenses[0]["amount"] == 10.0
    assert expenses[0]["category"] == "Shopping"
```

## Logging

The backend includes logging for database and application operations.

Logs are written to:

``` text
backend/server.log
```

The log file is generated at runtime and is excluded from Git using
`.gitignore`.

## Requirements

The main dependencies are pinned in `requirements.txt`:

``` text
pandas==3.0.6
streamlit==1.64.0
fastapi==0.141.1
pydantic==2.13.5
uvicorn==0.53.0
mysql-connector-python==26.7.0
requests==2.34.2
pytest==9.1.1
python-dotenv
```

## Application Screens

### Add / Update

The Add/Update interface provides:

-   Date selection
-   Expense amount input
-   Category selection
-   Notes input
-   Existing expense retrieval
-   Expense submission

### Analytics

The Analytics interface provides:

-   Start and end date selection
-   Category-wise expense totals
-   Bar chart visualization
-   Percentage contribution of each category
-   Analytics table

## Data Flow

``` text
User
  │
  ▼
Streamlit Frontend
  │
  │ HTTP Requests
  ▼
FastAPI
  │
  ▼
db_helper.py
  │
  │ SQL Queries
  ▼
MySQL Database
  │
  ▼
Expense Data
  │
  ▼
Analytics / UI
```

## Key Learning Areas

This project demonstrates practical use of:

-   Python project structure
-   REST API development with FastAPI
-   Pydantic models
-   Streamlit UI development
-   HTTP communication between frontend and backend
-   MySQL database connectivity
-   SQL aggregation using `SUM()` and `GROUP BY`
-   Date-range queries
-   Data processing with Pandas
-   Automated testing with Pytest
-   Application logging
-   Environment variable management
-   Separation of frontend, backend, database, and test code

## Future Improvements

Possible improvements include:

-   Add authentication and user-specific expenses
-   Add an expense ID for individual expense editing/deletion
-   Add monthly and yearly analytics
-   Add more visualization types
-   Add budget tracking and spending limits
-   Add CSV/Excel export
-   Add database transaction rollback/error handling
-   Expand frontend and API test coverage
-   Add deployment configuration

## Author

**Kshitish Nayak**

Built as a Python full-stack project to practice backend API
development, database integration, frontend development, analytics, and
testing.
