# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import sql


"""
Для тех, кто хочет запустить, предварительно нужно поставить postgresql.
затем создать юзера, поставить на него пароль.
Создать базу данных, а после дать все права на нее созданному юзеру.
И только после этого запускать функцию create_tables! Она создаст нужные таблицы.
"""


def create_tables(db, username, password, host, port):
    con = psycopg2.connect(dbname=db, user=username, host=host, port=port, password=password)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS spreadsheets(id SERIAL PRIMARY KEY, name VARCHAR(200),"
                "folder_id INTEGER, url VARCHAR(300) UNIQUE NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS students(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses(url VARCHAR(300) PRIMARY KEY, name VARCHAR(100) NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses_students(student VARCHAR(200) REFERENCES students,"
                " course VARCHAR(300) REFERENCES courses, PRIMARY KEY(student, course))")
    cur.execute("CREATE TABLE IF NOT EXISTS courseworks(form_url VARCHAR(300) PRIMARY KEY,"
                "course VARCHAR(300) REFERENCES courses, name VARCHAR(100),"
                "start_time timestamp NOT NULL, end_time timestamp NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS lecturers(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses_lecturers(lecturer VARCHAR(200) REFERENCES lecturers,"
                "course VARCHAR(300) REFERENCES courses, PRIMARY KEY(lecturer, course))")

    con.commit()
    cur.close()
    con.close()


def add_data_to_user_table(email, base_folder_id):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO user VALUES (?, ?)", (email, base_folder_id))
    # conn.commit()


def add_data_to_course_table(course_id, course_name, course_url, email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?)", (course_id, course_name, course_url, email))
    # conn.commit()


def add_data_to_spreadsheet_table(spreadsheet_id, spreadsheet_name, spreadsheet_url, email, folder_id):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO spreadsheet VALUES (?, ?, ?, ?, ?)",
    #                (spreadsheet_id, spreadsheet_name, spreadsheet_url, email, folder_id))
    # conn.commit()


def add_data_to_coursework_table(course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id,
                                 end_time):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO coursework VALUES (?, ?, ?, ?, ?, ?, ?)",
    #                (course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id, end_time))
    # conn.commit()
    # print("CW added")


def update_course_name(course_id, course_name):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("UPDATE course SET course_name=? WHERE course_id=?", (course_name, course_id))
    # conn.commit()


def update_base_folder_id(base_folder_id, email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("UPDATE user SET base_folder_id=? WHERE email=?", (base_folder_id, email))
    # conn.commit()


def search_for_user(email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM user WHERE email=?", (email,))
    # return cursor.fetchall()


def search_for_user_courses(email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM course WHERE email=?", (email,))
    # return cursor.fetchall()


def search_for_user_course_with_name(email, name):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM course WHERE email=? AND course_name=?", (email, name))
    # return cursor.fetchall()


def search_for_user_cmms(email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM spreadsheet WHERE email=?", (email,))
    # return cursor.fetchall()


def search_for_spreadsheet(spreadsheet_id):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM spreadsheet WHERE spreadsheet_id=?", (spreadsheet_id,))
    # return cursor.fetchall()


def search_for_unchecked_coursework():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM coursework WHERE datetime(end_time)<current_timestamp")
    # return cursor.fetchall()


def show_all_in_user_table():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM user")
    # return cursor.fetchall()


def show_all_in_course_table():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM course")
    # return cursor.fetchall()


def show_all_in_coursework_table():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM coursework")
    # return cursor.fetchall()


def show_all_in_spreadsheet_table():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM spreadsheet")
    # return cursor.fetchall()


def delete_course_from_table(course_id, email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM course WHERE course_id=? AND email=?", (course_id, email))
    # conn.commit()


def delete_coursework_from_table(form_url, student_id):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM coursework WHERE form_url=? AND student_id=?", (form_url, student_id))
    # conn.commit()


def delete_spreadsheet_from_table(spreadsheet_id, email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM spreadsheet WHERE spreadsheet_id=? AND email=?", (spreadsheet_id, email))
    # conn.commit()


def delete_all_in_tables():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM user")
    # cursor.execute("DELETE FROM course")
    # cursor.execute("DELETE FROM spreadsheet")
    # cursor.execute("DELETE FROM coursework")
    # conn.commit()


def delete_all_in_coursework_table():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DELETE FROM coursework")
    # conn.commit()


def drop_all_tables():
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("DROP TABLE user")
    # cursor.execute("DROP TABLE course")
    # cursor.execute("DROP TABLE spreadsheet")
    # cursor.execute("DROP TABLE coursework")
    # conn.commit()


if __name__ == '__main__':
    delete_all_in_coursework_table()
