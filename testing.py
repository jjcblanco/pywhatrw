from pprint import pprint
from ssl import ALERT_DESCRIPTION_UNRECOGNIZED_NAME
from Google import Create_Service

CLIENT_SECRET_FILE = 'D:\javier blanco\python\pywhatrw\client_secret_267771707-hi8fjjm3qtbgeqrg1n9c3gkehestnr21.apps.googleusercontent.com.json'
API_NAME = 'API Project'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/calendar/v3']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)








