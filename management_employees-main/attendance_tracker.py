import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # Use your MySQL username
    password="",        # Use your MySQL password
)

# Create a cursor object
cursor = conn.cursor()

# SQL statements to create a database and tables
create_database = "CREATE DATABASE IF NOT EXISTS attendance_tracker"
use_database = "USE attendance_tracker"

create_employees_table = """
CREATE TABLE IF NOT EXISTS employes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employes_id VARCHAR(10),
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);
"""

create_departments_table = """
CREATE TABLE IF NOT EXISTS departements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dept_id VARCHAR(10),
    dept_name VARCHAR(100)
);
"""

create_attendance_table = """
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employes_id VARCHAR(10),
    dept_id VARCHAR(10),
    timestamp DATETIME
);
"""

# Execute SQL statements
cursor.execute(create_database)
cursor.execute(use_database)
cursor.execute(create_employees_table)
cursor.execute(create_departments_table)
cursor.execute(create_attendance_table)

# Close the cursor and connection
cursor.close()
conn.close()

print("Database and tables created successfully!")
