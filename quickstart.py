from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# module for getting started with the gmail API from
# https://developers.google.com/gmail/api/quickstart/python

# more specifically, run this, changing the SCOPES if need be,
# whenever you need to create the credentials to log in

# two bugs on MAC OS to overcome:
# 1. fix xdg-settings: https://stackoverflow.com/questions/51348322/everytime-i-run-jupyter-notebook-why-i-always-got-this-on-mac-os
# 2. don't use safari, but copy URL into firefox

# If modifying these scopes, delete the file token.pickle.
SEND_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
READ_ONLY = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = [SEND_SCOPE, READ_ONLY]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()
