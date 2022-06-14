import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main(sample_range_name, sample_spreadsheet_id):

    creds = None

    if os.path.exists('token.pickle'):
        print("entro")
        with open('token.pickle', 'rb') as token:
            print("paso")
            #creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'D:\javier blanco\python\pywhatrw\client_secret_91639520408-d82vrf7rlbfuj1c8g3p87see7itjeq5s.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sample_spreadsheet_id,
                                range=sample_range_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        df = pd.DataFrame(values)
        df.columns = df.iloc[0]
        df.drop(df.index[0], inplace=True) 
        return df

df = main("Sheet1", "1Xr0fKkGxT4hA4qSJuziSOxBHcuRkLjUI5Exaae2FezE")