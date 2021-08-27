import hashlib
import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()

def create_database():
    StudentsTB='''
    CREATE TABLE IF NOT EXISTS Students(
        StudentID INTEGER AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        email VARCHAR(20),
        password VARCHAR(32)
    )
    '''
    LecturersTB='''
    CREATE TABLE IF NOT EXISTS Lecturers(
        LecturerID INTEGER AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        email VARCHAR(20),
        password VARCHAR(32)
    )
    '''
    AdminsTB='''
    CREATE TABLE IF NOT EXISTS Admins(
        AdminID INTEGER AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        email VARCHAR(20),
        password VARCHAR(32)
    )
    '''
    cur.execute(StudentsTB)
    cur.execute(LecturersTB)
    cur.execute(AdminsTB)

    students_sql_query = "INSERT OR IGNORE INTO Students (StudentID,first_name,last_name,email,password) VALUES (?, ?, ?, ?, ?)"

    lecturers_sql_query = "INSERT OR IGNORE INTO Lecturers (LecturerID,first_name,last_name,email,password) VALUES (?, ?, ?, ?, ?)"

    admins_sql_query = "INSERT OR IGNORE INTO Admins (AdminID,first_name,last_name,email,password) VALUES (?, ?, ?, ?, ?)"
    default_pass = b'1234'
    val = [
        ("1","Frederick","Omondi","frankomondi311@gmail.com",f"{hashlib.sha256(default_pass).hexdigest()}"),
        ("2","Dofften","Dofften","dofften@dofften.com",f"{hashlib.sha256(default_pass).hexdigest()}"),
        ("3","Omondi","Kiilu","omondi@kiilu.com",f"{hashlib.sha256(default_pass).hexdigest()}"),
    ]

    cur.executemany(students_sql_query, val)
    cur.executemany(lecturers_sql_query, val)
    cur.executemany(admins_sql_query, val)


    # cur.execute("SELECT * FROM Students")
    # rows = cur.fetchall()
    # for row in rows:
    #     print(row)
    conn.commit()
    cur.close()

    conn.close()


# create_database()