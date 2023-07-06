from oauth2client import client, file, tools
from apiclient import discovery
from httplib2 import Http
from googleapiclient.discovery import build

def get_creds(SCOPES, credentials, storage):
    store = file.Storage(storage)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_drive_service(creds):
    service = build('drive', 'v3', credentials=creds)
    return service

def get_forms_service(creds):
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
    service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
    return service