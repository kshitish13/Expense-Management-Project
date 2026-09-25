import mysql.connector
from contextlib import contextmanager
import logging
from logging_setup import setup_logger
from datetime import datetime

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):#by default commit is false whenever we insert or update the table we will do commit=true there
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOURPASSWORD",
        database="expense_manager"
    )


    cursor = connection.cursor(dictionary=True)
    yield  cursor

    connection.commit() # whenever we are inserting something we need to commit
    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        for expense in expenses:
            print(expense)




def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        print("Date received:", expense_date)
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with date : {expense_date}, amount : {amount}, category : {category} and notes : {notes}")
    with get_db_cursor(commit=True) as cursor: # we do commit=True here as we are updating the table
        cursor.execute(
            "INSERT INTO expenses (expense_date,amount,category,notes) VALUES (%s,%s,%s,%s)",
            (expense_date,amount,category,notes)
        )


def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start date : {start_date} and end date : {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expense_manager.expenses
            WHERE expense_date BETWEEN %s AND %s
            GROUP BY category
            """,
            (start_date, end_date)
        )

        data = cursor.fetchall()
        return data

def fetch_expense_by_month(month_name, year):
    month_number = datetime.strptime(month_name, "%B").month
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE MONTH(expense_date) = %s AND YEAR(expense_date) = %s",(month_number, year))
        expenses = cursor.fetchall()
        return expenses

def fetch_summary_for_month(month_name, year):
    month_number = datetime.strptime(month_name, "%B").month
    logger.info(f"Monthly summary for {month_name} called")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT category as Category,sum(amount) as Total FROM expenses WHERE MONTH(expense_date) = %s AND YEAR(expense_date) = %s group by category",(month_number, year))
        expenses = cursor.fetchall()
        return expenses



if __name__ == "__main__":
    #fetch_expenses_for_date("2024-08-01")
    #delete_expense_for_date("2024-08-25")
    summary=fetch_expense_summary('2026-08-01','2026-08-09')
    print("Printing summary")
    for data in summary:
        print(data)

    august_expense=fetch_expense_by_month("August",2026)
    print("Expense fo month")
    for expense in august_expense:
        print(expense)

    august_summary=fetch_summary_for_month("August",2026)
    print("Summary for month")
    for expense in august_summary:
        print(expense)