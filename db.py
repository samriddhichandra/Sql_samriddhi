import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="expense_db"
    )

def insert_expense(amount, category, description, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (%s, %s, %s, %s)",
        (amount, category, description, date)
    )
    conn.commit()
    conn.close()

def get_all_expenses():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, amount, category, description, date FROM expenses")
    return cursor.fetchall()

