import mysql.connector
import os

# Get DB credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    print("Database connected successfully!")
except mysql.connector.Error as e:
    print("Database connection failed:", e)
    conn = None
    cursor = None

# Login function
def login(data: tuple):
    if cursor is None:
        print("No database connection")
        return False
    try:
        q = "SELECT * FROM users_login WHERE email=%s AND password=%s"
        cursor.execute(q, data)
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(e)
        return False

# Signup function
def signup(data: tuple):
    if cursor is None:
        print("No database connection")
        return False
    try:
        sub_data = data[1:3]  # (email, password)
        if not login(sub_data):
            q = "INSERT INTO users_login (name, email, password, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(q, data)
            conn.commit()
            return cursor.rowcount > 0
        else:
            return False
    except Exception as e:
        print(e)
        return False
