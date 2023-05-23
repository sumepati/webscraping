from __future__ import print_function

import os.path
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient import discovery
import pygsheets
import pandas as pd


def update_sheet(title,df):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. This is boiler plate code and refered from Google API documentation
    # https://developers.google.com/sheets/api/quickstart/python
    # Follow the steps to Enable APIs and setup Project and credentials

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Spreadsheet created in your Google account, and used ID that is  unique
        spreadsheetId = 'sheetID'
        SAMPLE_RANGE_NAME = 'A1:D10000'
        df_google = pd.DataFrame()
        df_google =df

        service = discovery.build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }

        spreadsheet = service.spreadsheets().values().update(spreadsheetId=spreadsheetId,
                                                             valueInputOption='RAW',
                                                             range=SAMPLE_RANGE_NAME,
                                                             body=dict(
                                                                 majorDimension='ROWS',
                                                                 values=df_google.T.reset_index().T.values.tolist())
                                                             ).execute()
        print('Sheet successfully Updated')
        # print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
