from pprint import pprint
from ssl import ALERT_DESCRIPTION_UNRECOGNIZED_NAME
from Google import Create_Service

CLIENT_SECRET_FILE = './client_secret_91639520408-d82vrf7rlbfuj1c8g3p87see7itjeq5s.apps.googleusercontent.com.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

  # Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')


# Prints the start and name of the next 10 events
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])







