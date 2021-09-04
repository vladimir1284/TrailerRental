import datetime
from datetime import timedelta

import pytz

from google.oauth2 import service_account

from googleapiclient.discovery import build

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
from email import encoders
import base64
from apiclient import errors, discovery
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

service_account_email = "trailer-rental@trailer-rental-323614.iam.gserviceaccount.com"
credentials = service_account.Credentials.from_service_account_file('trailer-rental-323614-5eec73be91df.json')



def buildMailService():
   SCOPES = ['https://www.googleapis.com/auth/gmail.send']
   # scoped_credentials = credentials.with_scopes(SCOPES)
   # service = build('gmail', 'v1', credentials=scoped_credentials)
   creds = None
   # The file token.json stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.json'):
     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
     if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
     else:
         flow = InstalledAppFlow.from_client_secrets_file(
             'credentials.json', SCOPES)
         creds = flow.run_local_server(port=0)
     # Save the credentials for the next run
     with open('token.json', 'w') as token:
         token.write(creds.to_json())

   service = build('gmail', 'v1', credentials=creds)
   return service

def buildCalendarService():
   SCOPES = ["https://www.googleapis.com/auth/calendar"]
   scoped_credentials = credentials.with_scopes(SCOPES)
   service = build("calendar", "v3", credentials=scoped_credentials)
   return service


def create_event():
    service = buildCalendarService()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    # event = (
        # service.events()
        # .insert(
            # calendarId="trailerrentalweb@gmail.com",
            # body={
                # "summary": "Foo 2",
                # "description": "Bar",
                # "start": {"dateTime": start_datetime.isoformat()},
                # "end": {
                    # "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                # },
            # },
        # )
        # .execute()
    # )
    # event = {
              # 'summary': 'Google I/O 2015',
              # 'location': '800 Howard St., San Francisco, CA 94103',
              # 'description': 'A chance to hear more about Google\'s developer products.',
              # 'start': {
                # 'dateTime': '2021-09-28T09:00:00-07:00',
                # 'timeZone': 'America/Los_Angeles',
              # },
              # 'end': {
                # 'dateTime': '2021-09-28T17:00:00-07:00',
                # 'timeZone': 'America/Los_Angeles',
              # },
              # 'recurrence': [
                # 'RRULE:FREQ=DAILY;COUNT=2'
              # ],
              # 'reminders': {
                # 'useDefault': False,
                # 'overrides': [
                  # {'method': 'email', 'minutes': 24 * 60},
                  # {'method': 'popup', 'minutes': 10},
                # ],
              # },
            # }
    event = {'summary': 'Contract: El primero -> Ernesto Quintanilla termination', 'location': 'Somewhere', 'description': 'Contract finish alert. Check the details here https://drive.google.com/uc?id=1qzZQvUsP1OE2QC-lFqM4gq88yYbJGGea&export=download.', 'start': {'date': '2022-05-11', 'timeZone': 'America/Los_Angeles'}, 'end': {'date': '2022-05-11', 'timeZone': 'America/Los_Angeles'}, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': 1440}, {'method': 'popup', 'minutes': 720}]}}

    event = service.events().insert(calendarId='vladimir.rdguez@gmail.com', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    
def create_message(sender, to, subject, message_text):
     """Create a message for an email.

     Args:
       sender: Email address of the sender.
       to: Email address of the receiver.
       subject: The subject of the email message.
       message_text: The text of the email message.

     Returns:
       An object containing a base64url encoded email object.
     """
     message = MIMEText(message_text)
     message['to'] = to
     message['from'] = sender
     message['subject'] = subject
     return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
     
def create_message_with_attachment(sender, to, subject, message_text, file):
     """Create a message for an email.

     Args:
       sender: Email address of the sender.
       to: Email address of the receiver.
       subject: The subject of the email message.
       message_text: The text of the email message.
       file: The path to the file to be attached.

     Returns:
       An object containing a base64url encoded email object.
     """
     message = MIMEMultipart()
     message['to'] = to
     message['from'] = sender
     message['subject'] = subject

     msg = MIMEText(message_text)
     message.attach(msg)

     content_type, encoding = mimetypes.guess_type(file)

     if content_type is None or encoding is not None:
       content_type = 'application/octet-stream'
     main_type, sub_type = content_type.split('/', 1)
     if main_type == 'text':
       fp = open(file, 'rb')
       msg = MIMEText(fp.read(), _subtype=sub_type)
       fp.close()
     elif main_type == 'image':
       fp = open(file, 'rb')
       msg = MIMEImage(fp.read(), _subtype=sub_type)
       fp.close()
     elif main_type == 'audio':
       fp = open(file, 'rb')
       msg = MIMEAudio(fp.read(), _subtype=sub_type)
       fp.close()
     else:
       fp = open(file, 'rb')
       msg = MIMEBase(main_type, sub_type)
       msg.set_payload(fp.read())
       encoders.encode_base64(msg)
       fp.close()
     filename = os.path.basename(file)
     msg.add_header('Content-Type', main_type, name=filename)
     msg.add_header('Content-Disposition', 'attachment', filename=filename)
     message.attach(msg)

     return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')}
     
def send_message(service, user_id, message):
   """Send an email message.

   Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

   Returns:
    Sent Message.
   """
   try:
      message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
      print('Message Id: %s' % message['id'])
      return message
   except errors.HttpError as error:
      print('An error occurred: %s' % error)


      
#service = buildMailService()        
#message = create_message_with_attachment("trailerrentalweb@gmail.com", "vladimir.rdguez@gmail.com", "test", "Hola mundo con adjunto!", "vladimir.pdf")
#send_message(service, 'me', message)

create_event()
