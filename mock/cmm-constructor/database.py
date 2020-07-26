# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import sql


class Database(object):
    def __init__(self, db, username, host, port, password):
        """
        :param db: Название базы данных
        :param username: Юзер в бд
        :param host: Хост
        :param port: Порт
        :param password: Пароль
        """
        self.con = psycopg2.connect(dbname=db, user=username, host=host, port=port, password=password)

    def create_tables(self):
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS spreadsheets(s_name VARCHAR(200),"
                    "folder_id INTEGER, url VARCHAR(300) PRIMARY KEY,"
                    "lecturer VARCHAR(200) REFERENCES lecturers NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS students(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS courses(url VARCHAR(300) PRIMARY KEY, course_name VARCHAR(100) NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS courses_students(student VARCHAR(200) REFERENCES students,"
                    " course VARCHAR(300) REFERENCES courses, PRIMARY KEY(student, course))")
        cur.execute("CREATE TABLE IF NOT EXISTS courseworks(id SERIAL PRIMARY KEY, form_url VARCHAR(300) NOT NULL,"
                    "course VARCHAR(300) REFERENCES courses, coursework_name VARCHAR(100),"
                    "start_time timestamp NOT NULL, end_time timestamp NOT NULL)")
        cur.execute("CREATE TABLE IF NOT EXISTS lecturers(email VARCHAR(200) PRIMARY KEY, folder_id INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS courses_lecturers(lecturer VARCHAR(200) REFERENCES lecturers,"
                    "course VARCHAR(300) REFERENCES courses, PRIMARY KEY(lecturer, course))")

        self.con.commit()
        cur.close()
        print("**** CMM_CONSTRUCTOR_LOGS - file: " + __file__ + " - tables created ****")

    def add_data_to_student_course_table(self, course_name, course_url, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("INSERT INTO course VALUES ({url, course_name})")
                    .format(url=sql.Literal(course_url), course_name=sql.Literal(course_name)))
        cur.execute(sql.SQL("INSERT INTO courses_students VALUES ({course, student})")
                    .format(course=sql.Literal(course_url), student=sql.Literal(email)))
        self.con.commit()
        cur.close()

    def add_data_to_spreadsheet_table(self, spreadsheet_name, spreadsheet_url, email, folder):
        cur = self.con.cursor()
        cur.execute(sql.SQL("INSERT INTO spreadsheets VALUES ({s_name, url, lecturer, folder_id})")
                    .format(s_name=sql.SQL(spreadsheet_name), url=sql.Literal(spreadsheet_url),
                            lecturer=sql.Literal(email), folder_id=sql.Literal(folder)))
        self.con.commit()
        cur.close()

    def update_course_name(self, course, course_name):
        cur = self.con.cursor()
        cur.execute(sql.SQL("UPDATE course SET course_name = {new_name} WHERE url = {course_url}")
                    .format(new_name=sql.Literal(course_name), course_url=sql.Literal(course)))
        self.con.commit()
        cur.close()

    def search_for_lecturer(self, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM lecturers WHERE email = {lecturer_email}")
                    .format(lecturer_email=sql.Literal(email)))
        result = cur.fetchall()
        cur.close()
        return result

    def search_for_lecturer_courses(self, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM courses WHERE url IN"
                            "(SELECT course FROM courses_lectures WHERE email = {lecturer_email})")
                    .format(lecturer_email=sql.Literal(email)))
        result = cur.fetchall()
        cur.close()
        return result

    def search_for_user_course_with_name(self, email, name):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM courses WHERE url IN"
                            "(SELECT course FROM courses_lectures WHERE email = {lecturer_email})"
                            " AND course_name = {c_name}")
                    .format(lecturer_email=sql.Literal(email), c_name=sql.Literal(name)))
        result = cur.fetchall()
        cur.close()
        return result

    def search_for_user_cmms(self, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM spreadsheets WHERE lecturer = {lecturer_email}")
                    .format(lecturer_email=sql.Literal(email)))
        result = cur.fetchall()
        cur.close()
        return result

    def search_for_spreadsheet(self, spreadsheet_url):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM spreadsheets WHERE url = {s_url}")
                    .format(s_url=sql.Literal(spreadsheet_url)))
        result = cur.fetchall()
        cur.close()
        return result

    def update_base_folder_id(self, base_folder_id, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("UPDATE lecturers SET foder_id = {f_id} WHERE email = {lecturer_email}")
                    .format(f_id=sql.Literal(base_folder_id), lecturer_email=sql.Literal(email)))
        self.con.commit()

    def search_for_unchecked_coursework(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM courseworks WHERE end_time < current_timestamp"))
        result = cur.fetchall()
        cur.close()
        return result

    def add_data_to_user_table(self, email, base_folder_id):
        cur = self.con.cursor()
        cur.execute(sql.SQL("INSERT INTO lecturers VALUES ({email, folder_id})")
                    .format(email=sql.Literal(email), folder_id=sql.Literal(base_folder_id)))
        self.con.commit()
        cur.close()

    def show_all_in_user_table(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM lecturers"))
        result = cur.fetchall()
        cur.close()
        return result

    def show_all_in_course_table(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM courses"))
        result = cur.fetchall()
        cur.close()
        return result

    def show_all_in_coursework_table(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM courseworks"))
        result = cur.fetchall()
        cur.close()
        return result

    def show_all_in_spreadsheet_table(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("SELECT * FROM spreadsheets"))
        result = cur.fetchall()
        cur.close()
        return result

    def delete_course_from_table(self, course):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DELETE FROM courses_lectures WHERE course = {course_url}")
                    .format(course_url=sql.Literal(course)))
        cur.execute(sql.SQL("DELETE FROM courses_students WHERE course = {course_url}")
                    .format(course_url=sql.Literal(course)))
        cur.execute(sql.SQL("DELETE FROM courses WHERE url = {course_url}")
                    .format(course_url=sql.Literal(course)))
        self.con.commit()
        cur.close()

    def delete_coursework_from_table(self, form_url):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DELETE FROM courseworks WHERE form_url = {url}")
                    .format(url=sql.Literal(form_url)))
        self.con.commit()
        cur.close()

    def delete_spreadsheet_from_table(self, spreadsheet_url, email):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DELETE FROM spreadsheets WHERE url = {spreadsheet} AND lecturer = {email}")
                    .format(spreadsheet=sql.Literal(spreadsheet_url), email=sql.Literal(email)))
        self.con.commit()
        cur.close()

    def delete_all_in_tables(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DELETE FROM spreadsheets"))
        cur.execute(sql.SQL("DELETE FROM courseworks"))
        cur.execute(sql.SQL("DELETE FROM courses_lecturers"))
        cur.execute(sql.SQL("DELETE FROM lecturers"))
        cur.execute(sql.SQL("DELETE FROM courses_students"))
        cur.execute(sql.SQL("DELETE FROM students"))
        cur.execute(sql.SQL("DELETE FROM courses"))
        self.con.commit()
        cur.close()

    def delete_all_in_coursework_table(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DELETE FROM courseworks"))
        self.con.commit()
        cur.close()

    def drop_all_tables(self):
        cur = self.con.cursor()
        cur.execute(sql.SQL("DROP TABLE courses CASCADE"))
        cur.execute(sql.SQL("DROP TABLE courses_lecturers CASCADE"))
        cur.execute(sql.SQL("DROP TABLE courses_students CASCADE"))
        cur.execute(sql.SQL("DROP TABLE courseworks CASCADE"))
        cur.execute(sql.SQL("DROP TABLE students CASCADE"))
        cur.execute(sql.SQL("DROP TABLE lecturers CASCADE"))
        cur.execute(sql.SQL("DROP TABLE spreadsheets CASCADE"))
        self.con.commit()
        cur.close()


def add_data_to_coursework_table(con, coursework_id, url, course, grade_coursework_id,
                                 end_time):
    pass
    # cur = con.cursor()
    # cur.execute(sql.SQL("INSERT INTO courseworks VALUES {id, form_url, course}"))
    # TODO: Разобраться, что такое grade_coursework_id, из названия не сильно понятно
    # cursor.execute("INSERT INTO coursework VALUES (?, ?, ?, ?, ?, ?, ?)",
    #                (course_id, coursework_id, form_url, student_email, student_id, grade_coursework_id, end_time))
    # conn.commit()
    # print("CW added")


if __name__ == '__main__':
    print("It's wednesday dude!")
