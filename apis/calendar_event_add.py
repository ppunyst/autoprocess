from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def calendar_add(data):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console() #flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
        
    event = {
        'summary': '게스트 ' + data['name'] + ' 예약',
        'start': {
            'dateTime': data['start_date'],
        },
        'end': {
            'dateTime': data['end_date'],
        }
    }

    # 선빈님 venue yeonnam: '6iov0erdjnq0vuk41kvuvd1f64@group.calendar.google.com' # 'primary'
    # 선빈님 the teras: 'a4dbhgu2qfas55aofflcmv3vh0@group.calendar.google.com' # '3i018h05h63rv0d9fgi97lfias@group.calendar.google.com'
    cal_Id = '6iov0erdjnq0vuk41kvuvd1f64@group.calendar.google.com' if data['place'] == '베뉴 연남' else 'a4dbhgu2qfas55aofflcmv3vh0@group.calendar.google.com' 
    
    event = service.events().insert(calendarId=cal_Id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


    

        
