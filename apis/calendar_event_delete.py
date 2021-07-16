from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def calendar_delete(data):
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
            creds = flow.run_console() # flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    cal_Id = '6iov0erdjnq0vuk41kvuvd1f64@group.calendar.google.com' if data['place'] == '베뉴 연남' else 'a4dbhgu2qfas55aofflcmv3vh0@group.calendar.google.com' 
    timeMin = data['start_date']

    print('Getting the upcoming events')
    events_result = service.events().list(calendarId=cal_Id, timeMin=timeMin, orderBy='startTime', singleEvents=True).execute()
    event = events_result.get('items', [])[0]
    print(event)
    if data['name'] in event['summary']:
        name = event['summary']
        service.events().delete(calendarId=cal_Id, eventId=event['id']).execute()
        print('%s is deleted' % name)
    # if not events:
    #     print('No upcoming events found.')

    # for event in events:
    #     print(event)
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    
    
