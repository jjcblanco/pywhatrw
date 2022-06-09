from pprint import pprint
from ssl import ALERT_DESCRIPTION_UNRECOGNIZED_NAME
from Google import Create_Service

CLIENT_SECRET_FILE = './client_secret_91639520408-d82vrf7rlbfuj1c8g3p87see7itjeq5s.apps.googleusercontent.com.json'
API_NAME = 'pythonapp'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/calendar.events','https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

print(dir(service))







