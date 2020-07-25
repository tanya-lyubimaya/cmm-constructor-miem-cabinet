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
    cur.execute("CREATE TABLE IF NOT EXISTS spreadsheets(s_name VARCHAR(200),"
                "folder_id INTEGER, url VARCHAR(300) PRIMARY KEY,"
                "lecturer VARCHAR(200) REFERENCES lecturers NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS students(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses(url VARCHAR(300) PRIMARY KEY, course_name VARCHAR(100) NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses_students(student VARCHAR(200) REFERENCES students,"
                " course VARCHAR(300) REFERENCES courses, PRIMARY KEY(student, course))")
    cur.execute("CREATE TABLE IF NOT EXISTS courseworks(id SERIAL PRIMARY KEY, form_url VARCHAR(300) NOT NULL,"
                "course VARCHAR(300) REFERENCES courses, coursework_name VARCHAR(100),"
                "start_time timestamp NOT NULL, end_time timestamp NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS lecturers(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS courses_lecturers(lecturer VARCHAR(200) REFERENCES lecturers,"
                "course VARCHAR(300) REFERENCES courses, PRIMARY KEY(lecturer, course))")

    con.commit()
    cur.close()
    print("**** CMM_CONSTRUCTOR_LOGS - file: " + __file__ + " - tables created ****")
    return con


def add_data_to_user_table(email, base_folder_id):
    pass
    # cursor = conn.cursor() Я пока не знаю надо ли оно, возможно надо будет переписывать.
    # cursor.execute("INSERT INTO user VALUES (?, ?)", (email, base_folder_id))
    # conn.commit()


def add_data_to_student_course_table(con, course_name, course_url, email):
    """
    Чтобы избежать sql инъекций, следует использовать метод format в сочетании с классом sql и его методами
    """
    cur = con.cursor()
    cur.execute(sql.SQL("INSERT INTO course VALUES {url, course_name}")
                   .format(url=sql.Literal(course_url), course_name=sql.Literal(course_name)))
    cur.execute(sql.SQL("INSERT INTO courses_students VALUES {course, student}")
                .format(course=sql.Literal(course_url), student=sql.Literal(email)))
    con.commit()
    cur.close()


def add_data_to_spreadsheet_table(con, spreadsheet_name, spreadsheet_url, email, folder):
    cur = con.cursor()
    cur.execute(sql.SQL("INSERT INTO spreadsheets VALUES {s_name, url, lecturer, folder_id}")
                .format(s_name=sql.SQL(spreadsheet_name), url=sql.Literal(spreadsheet_url),
                        lecturer=sql.Literal(email), folder_id=sql.Literal(folder)))
    con.commit()
    cur.close()


def add_data_to_coursework_table(con, coursework_id, url, course, grade_coursework_id,
                                 end_time):
    cur = con.cursor()
    # cur.execute(sql.SQL("INSERT INTO courseworks VALUES {id, form_url, course}"))
    # TODO: Разобраться, что такое grade_coursework_id, из названия не сильно понятно
    # cursor.execute("INSERT INTO coursework VALUES (?, ?, ?, ?, ?, ?, ?)",
    #                (course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id, end_time))
    # conn.commit()
    # print("CW added")


def update_course_name(con, course, course_name):
    cur = con.cursor()
    cur.execute(sql.SQL("UPDATE course SET course_name = {new_name} WHERE url = {course_url}")
                .format(new_name=sql.Literal(course_name), course_url=sql.Literal(course)))
    con.commit()
    cur.close()


def update_base_folder_id(base_folder_id, email):
    pass
    # conn = sqlite3.connect('database.db')
    # cursor = conn.cursor()
    # cursor.execute("UPDATE user SET base_folder_id=? WHERE email=?", (base_folder_id, email))
    # conn.commit()


def search_for_lecturer(con, email):
    cur = con.cursor()
    cur.execute(sql.SQL("SELECT * FROM lecturers WHERE email = {lecturer_email}")
                .format(lecturer_email=sql.Literal(email)))
    result = cur.fetchall()
    cur.close()
    return result


def search_for_lecturer_courses(con, email):
    cur = con.cursor()
    cur.execute(sql.SQL("SELECT * FROM courses WHERE url IN"
                "(SELECT course FROM courses_lectures WHERE email = {lecturer_email})")
                .format(lecturer_email=sql.Literal(email)))
    result = cur.fetchall()
    cur.close()
    return result


def search_for_user_course_with_name(con, email, name):
    cur = con.cursor()
    cur.execute(sql.SQL("SELECT * FROM courses WHERE url IN"
                "(SELECT course FROM courses_lectures WHERE email = {lecturer_email}) AND course_name = {c_name}")
                .format(lecturer_email=sql.Literal(email), c_name=sql.Literal(name)))
    result = cur.fetchall()
    cur.close()
    return result


def search_for_user_cmms(con, email):
    cur = con.cursor()
    cur.execute(sql.SQL("SELECT * FROM spreadsheets WHERE lecturer = {lecturer_email}")
                .format(lecturer_email=sql.Literal(email)))
    result = cur.fetchall()
    cur.close()
    return result


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
