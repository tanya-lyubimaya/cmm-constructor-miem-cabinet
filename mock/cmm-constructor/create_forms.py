# -*- coding: utf-8 -*-

import socket
import pickle
from googleapiclient.discovery import build

socket.setdefaulttimeout(120)

MANIFEST = '''
{
    "timeZone": "Europe/Moscow",
    "exceptionLogging": "STACKDRIVER",
    "executionApi": {
        "access": "ANYONE"
    }
}
'''.strip()


def fulfill_forms(form_url, spreadsheet_id, questions):
    with open("classtoken.pickle", 'rb') as token:
        creds = pickle.load(token)
    app_service = build('script', 'v1', credentials=creds)

    script_id = "1LbejwBAbrFkgQfVW0V7XgQ4Vmu1aXZjRBmkHKRIwps1IewEXRUFti9fC"
    body = {
        "function": "fulfill",
        "devMode": True,
        "parameters": [form_url, spreadsheet_id, questions]
    }

    app_service.scripts().run(scriptId=script_id, body=body).execute()
    return print('Form was successfully fulfilled')


def set_grades(course_id, form_url, student_email, student_id, coursework_id):
    with open("classtoken.pickle", 'rb') as token:
        creds = pickle.load(token)
    app_service = build('script', 'v1', credentials=creds)

    script_id = "1LbejwBAbrFkgQfVW0V7XgQ4Vmu1aXZjRBmkHKRIwps1IewEXRUFti9fC"
    body = {
        "function": "setGrades",
        "devMode": True,
        "parameters": [course_id, form_url, student_email, student_id, coursework_id]
    }

    app_service.scripts().run(scriptId=script_id, body=body).execute()
    return print('User grade was successfully set')


def update_script():
    script_id = "1LbejwBAbrFkgQfVW0V7XgQ4Vmu1aXZjRBmkHKRIwps1IewEXRUFti9fC"
    script_file_name = "code"

    with open("classtoken.pickle", 'rb') as token:
        creds = pickle.load(token)
    app_service = build('script', 'v1', credentials=creds)

    with open(script_file_name, 'r') as f:
        sample_code = f.read()

    request = {
        'files': [{
            'name': 'code',
            'type': 'SERVER_JS',
            'source': sample_code
        }, {
            'name': 'appsscript',
            'type': 'JSON',
            'source': MANIFEST
        }
        ]
    }

    app_service.projects().updateContent(body=request, scriptId=script_id).execute()
    return print('Project was successfully updated')


if __name__ == '__main__':
    update_script()

