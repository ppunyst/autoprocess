from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def sheet_delete(db_data):
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]

    json_file_name = 'venueyeonnam-81da0907980b.json' #'automatic-process-313511-cb10e4dfb3fe.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)

    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/19NH5Yzf3nZ816bHDJdQ22dxrgT7edYp4flH8c9VClV0/edit#gid=0' # 'https://docs.google.com/spreadsheets/d/1YinD51DxRrHkbwQNSeRcPFGI7LiaFQPP9uVtQpEf0bQ/edit#gid=0'

    # 스프레스시트 문서 가져오기 
    doc = gc.open_by_url(spreadsheet_url)

    # 시트 선택하기
    worksheet = doc.worksheet('시트1')

    doc = gc.open_by_url(spreadsheet_url)
    # 시트 선택하기
    worksheet = doc.worksheet('시트1')
    # row_data = worksheet.row_values(1)
    # print(row_data)
    cell = worksheet.find(db_data['id'])
    worksheet.update_acell('J'+str(cell.row), db_data['status'])

    print('Google spread sheet - 삭제 업데이트 완료')