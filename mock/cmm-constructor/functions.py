# -*- coding: utf-8 -*-

import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from random import randint
import datetime
from create_forms import fulfill_forms, set_grades
from database import Database


SCOPES = ["https://www.googleapis.com/auth/forms",
          "https://www.googleapis.com/auth/script.send_mail",
          "https://www.googleapis.com/auth/script.projects",
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.appdata",
          "https://www.googleapis.com/auth/drive.file",
          "https://www.googleapis.com/auth/drive.metadata.readonly",
          "https://www.googleapis.com/auth/drive.readonly",
          "https://www.googleapis.com/auth/drive.scripts",
          "https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/classroom.announcements",
          "https://www.googleapis.com/auth/classroom.courses",
          "https://www.googleapis.com/auth/classroom.coursework.me",
          "https://www.googleapis.com/auth/classroom.coursework.students",
          "https://www.googleapis.com/auth/classroom.guardianlinks.students",
          "https://www.googleapis.com/auth/classroom.profile.emails",
          "https://www.googleapis.com/auth/classroom.profile.photos",
          "https://www.googleapis.com/auth/classroom.rosters",
          "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
          "https://www.googleapis.com/auth/classroom.topics",
          "https://www.googleapis.com/auth/admin.directory.user",
          "https://www.googleapis.com/auth/admin.directory.group"]
CLASS_BASE_FOLDER_ID = "15lsOxH0dPeD0tuHVR3GGgZd8z-SSbjhp"
FORM_PATTERN_ID = "1LGPQZTOPdDTCUJs6Tt_3mw_n_pQl-7Xkh1BZSpBrKTY"
SPREADSHEET_PATTERN_ID = "195PvzFmp2iBcQpiQuloV9W6rDduVay277O3OvVezN4M"


def get_credentials_for_class():
    creds = None
    if os.path.exists("classtoken.pickle"):
        with open("classtoken.pickle", 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("classtoken.pickle", 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_classroom_service():
    classroom_service = build('classroom', 'v1', credentials=get_credentials_for_class())
    return classroom_service


def get_drive_service():
    drive_service = build('drive', 'v3', credentials=get_credentials_for_class())
    return drive_service


def get_spreadsheet_service():
    spreadsheet_service = build('sheets', 'v4', credentials=get_credentials_for_class())
    return spreadsheet_service


def get_directory_service():
    directory_service = build('admin', 'directory_v1', credentials=get_credentials_for_class())
    return directory_service


# to find base folder id and set the variable CLASS_BASE_FOLDER_ID
def get_base_folder_id():
    drive_service = get_drive_service()
    request = "mimeType='application/vnd.google-apps.folder' and trashed=false and name='База КИМов'"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])
    return print(files)


# to find pattern form id and set the variable PATTERN_FORM_ID
def get_form_pattern_id():
    drive_service = get_drive_service()
    request = "mimeType='application/vnd.google-apps.form' and trashed=false and name='Шаблон формы'"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])
    return print(files)


# to find pattern form id and set the variable PATTERN_FORM_ID
def get_spreadsheet_pattern_id():
    drive_service = get_drive_service()
    request = "mimeType='application/vnd.google-apps.spreadsheet' and trashed=false and name='Шаблон таблицы'"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])
    return print(files)


def authorization(db, user_email):
    result = db.search_for_lecturer(user_email)
    if len(result) == 0:
        db.add_data_to_user_table(user_email, "")


def get_user_courses(db, user_email):
    check_and_update_course_table(db, user_email)
    courses_in_database = db.search_for_lecturer_courses(user_email)
    courses = []

    if len(courses_in_database) != 0:
        for course in courses_in_database:
            data = {
                "courseName": course[1],
                "courseUrl": course[0]
            }
            courses.append(data)

    return courses


def check_and_update_course_table(db, user_email):
    classroom_service = get_classroom_service()
    results = classroom_service.courses().list(teacherId=user_email).execute()
    courses_from_classroom = results.get('courses', [])
    courses_from_database = db.search_for_lecturer_courses(user_email)

    for course_from_classroom in courses_from_classroom:
        flag = False

        for course_from_database in courses_from_database:
            if course_from_classroom['alternateLink'] == course_from_database[0]:
                if course_from_classroom['name'] != course_from_database[1]:
                    db.update_course_name(course_from_database[0], course_from_classroom['name'])
                flag = True
                break

        if not flag:
            db.add_data_to_course_table(course_from_classroom['name'],
                                        course_from_classroom['alternateLink'], user_email)

    courses_from_database = db.search_for_lecturer_courses(user_email)

    for course_from_database in courses_from_database:
        flag = False

        for course_from_classroom in courses_from_classroom:
            if course_from_classroom['alternateLink'] == course_from_database[0]:
                flag = True
                break

        if not flag:
            db.delete_course_from_table(course_from_database[0])

    return print("Courses table updated")


def get_user_cmms(db, user_email):
    results = db.search_for_lecturer(user_email)
    cmms = []

    if results[0][1] != "":
        cmms_from_database = db.search_for_user_cmms(user_email)

        for cmm in cmms_from_database:
            data = {
                "spreadsheetId": cmm[0],
                "spreadsheetName": cmm[1],
                "spreadsheetUrl": cmm[2]
            }
            cmms.append(data)

    return cmms


def create_user_base_folder(db, drive_service, user_email):
    parent_folder = CLASS_BASE_FOLDER_ID
    folder_name = user_email.split('@')[0]

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder]
    }

    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')
    db.update_base_folder_id(folder_id, user_email)

    return folder_id


def create_spreadsheet(name, base_folder_id, drive_service, user_email):
    file_metadata = {
        'name': name,
        'parents': [base_folder_id]
    }
    spreadsheet = drive_service.files().copy(fileId=SPREADSHEET_PATTERN_ID, body=file_metadata,
                                             fields='id, name, webViewLink').execute()
    spreadsheet_id = spreadsheet.get('id')

    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user_email,
    }
    drive_service.permissions().create(fileId=spreadsheet_id, body=permission).execute()

    return [spreadsheet_id, spreadsheet.get('name'), spreadsheet.get('webViewLink')]


def create_folder_for_cmm_variants(name, parent, drive_service, user_email):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent]
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')

    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': user_email,
    }
    drive_service.permissions().create(fileId=folder_id, body=permission).execute()

    return folder_id


def create_cmm(db, name, user_email):
    drive_service = get_drive_service()
    result = db.search_for_lecturer(user_email)

    if result[0][1] == "":
        base_folder_id = create_user_base_folder(drive_service, user_email)
    else:
        base_folder_id = result[0][1]

    print(base_folder_id)

    spreadsheet = create_spreadsheet(name, base_folder_id, drive_service, user_email)
    folder_id = create_folder_for_cmm_variants(spreadsheet[0], base_folder_id, drive_service, user_email)
    db.add_data_to_spreadsheet_table(spreadsheet[0], spreadsheet[1], spreadsheet[2], user_email, folder_id)

    print("New CMM created")
    return print("New CMM created")


def delete_cmm(db, spreadsheet_id, user_email):
    drive_service = get_drive_service()

    spreadsheet = db.search_for_spreadsheet(spreadsheet_id)
    folder_id = spreadsheet[0][4]

    db.delete_spreadsheet_from_table(spreadsheet_id, user_email)

    drive_service.files().delete(fileId=spreadsheet_id).execute()
    drive_service.files().delete(fileId=folder_id).execute()

    return print("CMM deleted")


def get_info_about_spreadsheet(spreadsheet_id):
    spreadsheet_service = get_spreadsheet_service()
    ranges = []
    include_grid_data = True
    response = spreadsheet_service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                                      ranges=ranges,
                                                      includeGridData=include_grid_data).execute()
    sheets = response.get('sheets')
    amount_of_questions_per_sheet = []

    for sheet in sheets:
        title = (sheet.get('properties')).get('title')

        range_title = "'" + title + "'!B2:M"
        response = spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                   range=range_title).execute()
        row_amount = len(response.get('values'))
        amount_of_questions_per_sheet.append({"title": title, "questionsAmount": row_amount})

    return amount_of_questions_per_sheet


def create_forms(db, questions, amount, spreadsheet_id):
    drive_service = get_drive_service()

    spreadsheet = db.search_for_spreadsheet(spreadsheet_id)
    folder_id = spreadsheet[0][4]

    request = "mimeType='application/vnd.google-apps.form' and trashed=false and '" + folder_id + "' in parents"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])
    quantity = len(files) + 1

    for i in range(quantity, int(amount) + quantity):
        title = "Вариант " + str(i)
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        form = drive_service.files().copy(fileId=FORM_PATTERN_ID, body=file_metadata,
                                          fields='id, name, webViewLink').execute()

        fulfill_forms(form.get('webViewLink'), spreadsheet_id, questions)

    return print("Forms created")


def give_out_forms(db, folder_id, course_name, task_name, start_date, start_time, end_date, end_time, user_email):
    drive_service = get_drive_service()
    classroom_service = get_classroom_service()

    result = db.search_for_user_course_with_name(user_email, course_name)
    course_id = result[0][0]

    request = "mimeType='application/vnd.google-apps.form' and trashed=false and '" + folder_id + "' in parents"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id, webViewLink)').execute()
    forms = response.get('files', [])
    amount = len(forms)

    response = classroom_service.courses().students().list(courseId=course_id).execute()
    students = response.get('students', [])

    # start date in format 0001-01-01T00:00:00Z
    start_time = str(start_time).split(':')
    hours = int(start_time[0]) - 3
    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    minutes = int(start_time[1])
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    start_datetime = start_date + "T" + hours + ":" + minutes + ":00Z"

    # end date in format 2014-06-15 11:00:00
    end_date_mass = str(end_date).split('-')
    due_date = {"year": int(end_date_mass[0]), "month": int(end_date_mass[1]), "day": int(end_date_mass[2])}
    end_time = str(end_time).split(':')
    hours = int(end_time[0]) - 3
    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    minutes = int(end_time[1])
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    due_time = {"hours": int(end_time[0]) - 3, "minutes": int(end_time[1]), "seconds": 0, "nanos": 0}
    end_time_to_table = end_date + " " + hours + ":" + minutes + ":00"

    # create coursework for students grades
    coursework = {
        'title': task_name,
        'workType': 'ASSIGNMENT',
        'state': 'DRAFT',
        'dueDate': due_date,
        'dueTime': due_time,
        'scheduledTime': start_datetime,
        'maxPoints': 100
    }
    result = classroom_service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
    grades_coursework_id = result.get('id')

    # create students personal assignments
    for student in students:
        user_id = student.get('userId')
        student_name = ((student.get('profile')).get('name')).get('fullName')
        student_email = (student.get('profile')).get('emailAddress')
        title = task_name + " (" + student_name + ")"
        num = randint(0, amount-1)
        coursework = {
            'title': title,
            'materials': [
                {'link': {'url': forms[num].get('webViewLink')}}
            ],
            'workType': 'ASSIGNMENT',
            'state': 'DRAFT',
            'dueDate': due_date,
            'dueTime': due_time,
            'scheduledTime': start_datetime,
            'maxPoints': 100
        }
        result = classroom_service.courses().courseWork().create(courseId=course_id, body=coursework).execute()
        coursework_id = result.get('id')

        body = {"assigneeMode": "INDIVIDUAL_STUDENTS",
                "modifyIndividualStudentsOptions": {"addStudentIds": [user_id]}}
        classroom_service.courses().courseWork().modifyAssignees(courseId=course_id, id=coursework_id, body=body).execute()
        # TODO: тут точно работает неправильно и нужно исправить
        db.add_data_to_coursework_table(course_id, coursework_id, forms[num].get('webViewLink'), student_email,
                                     user_id, grades_coursework_id, end_time_to_table)


def get_folder_url(db, spreadsheet_id, user_email):
    drive_service = get_drive_service()

    result = db.search_for_user(user_email)
    base_folder_id = result[0][1]

    request = "mimeType='application/vnd.google-apps.folder' and name='" + spreadsheet_id + "' and trashed=false and '" \
              + base_folder_id + "' in parents"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id, webViewLink)').execute()
    folder = response.get('files', [])
    folder_url = folder[0].get('webViewLink')

    return folder_url


def delete_forms(db, spreadsheet_id):
    drive_service = get_drive_service()

    spreadsheet = db.search_for_spreadsheet(spreadsheet_id)
    folder_id = spreadsheet[0][4]

    request = "trashed=false and '" + folder_id + "' in parents"
    response = drive_service.files().list(q=request, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])

    for file in files:
        file_id = file.get('id')
        drive_service.files().delete(fileId=file_id).execute()

    return print("Files deleted")


def delete_coursework_from_course(course_id, coursework_id):
    classroom_service = get_classroom_service()
    classroom_service.courses().courseWork().delete(courseId=course_id, id=coursework_id).execute()

# TODO: да кто такие ваши грейдс?


def set_grades_in_coursework():
    db = Database(db='cmm_constructor', username='cmm_admin', host='localhost', port='5432', password='Atlirgsu0')
    courseworks = db.search_for_unchecked_coursework()

    if courseworks:
        print(courseworks)

        for coursework in courseworks:
            set_grades(coursework[0], coursework[2], coursework[3], coursework[4], coursework[5])
            delete_coursework_from_course(coursework[0], coursework[1])
            db.delete_coursework_from_table(coursework[2], coursework[4])
        return print("Grades set")

    else:
        return print("No courseworks")


if __name__ == '__main__':
    get_info_about_spreadsheet()

