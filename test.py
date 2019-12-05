import gspread
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.discovery import build

from flask import request

values = [['DRCATCHER_FP[C_TIER]', 1, 'DHL','UNITED STATES']]
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '10V8_ahKyjNjy7yXxPEbFvou08ZHZJdjiyw41T4ZEZu4'
credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/MMT/Downloads/My Project 71063-3df5c85644c9.json',SCOPES)
http_auth = credentials.authorize(Http())
service = build('sheets','v4',http= http_auth)

def main():
    body = {'values': values}

    credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/MMT/Downloads/My Project 71063-3df5c85644c9.json',SCOPES)

    http_auth = credentials.authorize(Http())

    service = build('sheets','v4',http= http_auth)


    write_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID ,
                                                     range='Dashboard!A2:D2', #2
                                                     valueInputOption='RAW', body=body)
    write_result.execute()
    read()

def read():
    read_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                      range='Dashboard!A2:G2').execute()
    answers = read_result.get('values',[])
    if not answers:
        print('No data found.')
    else:
        print('project,quantity,fee:')
        for row in answers:
            print('%s,%s,%s'%(row[0],row[1],row[6]))

if __name__ == '__main__':
    main()

# gc = gspread.authorize(credentials)

# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/10V8_ahKyjNjy7yXxPEbFvou08ZHZJdjiyw41T4ZEZu4/edit#gid=1177088386'

# doc = gc.open_by_url(spreadsheet_url)

# worksheet = doc.worksheet('DASHBOARD')

# Celldata = worksheet.acell('G2').value
# print(Celldata)
