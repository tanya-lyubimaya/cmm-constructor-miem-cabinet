# -*- coding: utf-8 -*-

import sqlite3


def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE user (email text primary key, base_folder_id text)")
    cursor.execute('''CREATE TABLE course (course_id text, course_name text, course_url text, email text,
                      foreign key (email) references user(email))''')
    cursor.execute('''CREATE TABLE spreadsheet (spreadsheet_id text, spreadsheet_name text, spreadsheet_url text, 
                      email text, folder_id text,
                      foreign key (email) references user(email))''')
    cursor.execute('''CREATE TABLE coursework (course_id text, coursework_id text, form_url text, student_email text, 
                          student_id text, grade_coursework_id text, end_time text)''')
    conn.commit()


def add_data_to_user_table(email, base_folder_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user VALUES (?, ?)", (email, base_folder_id))
    conn.commit()


def add_data_to_course_table(course_id, course_name, course_url, email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?)", (course_id, course_name, course_url, email))
    conn.commit()


def add_data_to_spreadsheet_table(spreadsheet_id, spreadsheet_name, spreadsheet_url, email, folder_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO spreadsheet VALUES (?, ?, ?, ?, ?)", (spreadsheet_id, spreadsheet_name, spreadsheet_url, email, folder_id))
    conn.commit()


def add_data_to_coursework_table(course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id, end_time):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO coursework VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id, end_time))
    conn.commit()
    print("CW added")


def update_course_name(course_id, course_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE course SET course_name=? WHERE course_id=?", (course_name, course_id))
    conn.commit()


def update_base_folder_id(base_folder_id, email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET base_folder_id=? WHERE email=?", (base_folder_id, email))
    conn.commit()


def search_for_user(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE email=?", (email,))
    return cursor.fetchall()


def search_for_user_courses(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE email=?", (email,))
    return cursor.fetchall()


def search_for_user_course_with_name(email, name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course WHERE email=? AND course_name=?", (email, name))
    return cursor.fetchall()


def search_for_user_cmms(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spreadsheet WHERE email=?", (email,))
    return cursor.fetchall()


def search_for_spreadsheet(spreadsheet_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spreadsheet WHERE spreadsheet_id=?", (spreadsheet_id,))
    return cursor.fetchall()


def search_for_unchecked_coursework():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coursework WHERE datetime(end_time)<current_timestamp")
    return cursor.fetchall()


def show_all_in_user_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()


def show_all_in_course_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    return cursor.fetchall()


def show_all_in_coursework_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM coursework")
    return cursor.fetchall()


def show_all_in_spreadsheet_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spreadsheet")
    return cursor.fetchall()


def delete_course_from_table(course_id, email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course WHERE course_id=? AND email=?", (course_id, email))
    conn.commit()


def delete_coursework_from_table(form_url, student_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coursework WHERE form_url=? AND student_id=?", (form_url, student_id))
    conn.commit()


def delete_spreadsheet_from_table(spreadsheet_id, email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spreadsheet WHERE spreadsheet_id=? AND email=?", (spreadsheet_id, email))
    conn.commit()


def delete_all_in_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user")
    cursor.execute("DELETE FROM course")
    cursor.execute("DELETE FROM spreadsheet")
    cursor.execute("DELETE FROM coursework")
    conn.commit()


def delete_all_in_coursework_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM coursework")
    conn.commit()


def drop_all_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE user")
    cursor.execute("DROP TABLE course")
    cursor.execute("DROP TABLE spreadsheet")
    cursor.execute("DROP TABLE coursework")
    conn.commit()


if __name__ == '__main__':
    delete_all_in_coursework_table()

