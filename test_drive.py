from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account


def main():
   service_account_email = "trailer-rental@trailer-rental-323614.iam.gserviceaccount.com"
   credentials = service_account.Credentials.from_service_account_file('trailer-rental-323614-5eec73be91df.json')
   SCOPES = ['https://www.googleapis.com/auth/drive']
   scoped_credentials = credentials.with_scopes(SCOPES)
   service = build('drive', 'v3', credentials=scoped_credentials)

   # Call the Drive v3 API
   results = service.files().list(
      pageSize=10, fields="nextPageToken, files(id, name)").execute()
   items = results.get('files', [])

   if not items:
      print('No files found.')
   else:
      print('Files:')
      for item in items:
         print(u'{0} ({1})'.format(item['name'], item['id']))
         
   file_id = '1I5ljzcmY8V4c6SzWd8h9rtWmggUqd5qg'
   def callback(request_id, response, exception):
       if exception:
           # Handle error
           print(exception)
       else:
           print("Permission Id: %s" % response.get('id'))

   batch = service.new_batch_http_request(callback=callback)
   user_permission = {
       'type': 'user',
       'role': 'reader',
       'emailAddress': 'trailerrentalweb@gmail.com'
   }
   batch.add(service.permissions().create(
           fileId=file_id,
           body=user_permission,
           fields='id',
   ))
   batch.execute()

if __name__ == '__main__':
    main()
