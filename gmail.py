import os
import pickle
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mimetypes
from email.mime.image import MIMEImage

from googleapiclient.discovery import build

# module for doing stuff with gmail API

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
    # return {'raw': base64.urlsafe_b64encode(message.as_string().encode())}
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    return body
  
def create_message_with_attachment(
    sender, to, subject, message_text, file):
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
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    # return {'raw': base64.urlsafe_b64encode(message.as_string())}
    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

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
      message = (service.users().messages().send(userId=user_id, body=message).execute())
        
      print ('Message Id: %s' % message['id'])
      return message
  except: # errors.HttpError, error:
      print ('An error occurred: %s' % error)

def getService():
    "Returns gmail api unless token.pickl can't be found"

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        return None

    return build('gmail', 'v1', credentials=creds)

def getUnReadMessages():
    "Return the messages that have not been read in INBOX"

    service = getService()

    user = 'me'
    lableIds=['INBOX']

    # ignore the social and promotoions labels
    q = "is:unread in:inbox -category:{social promotions}"

    # get handles to the unread messages
    results = service.users().messages().list(userId=user, labelIds=lableIds, q=q).execute()
    messages = results.get('messages', [])

    if not messages:
        print("NO Messages!")
        return None
    else:
        print("You have %d unread messages" % len(messages)) 
        msgs = [] 
        for m in messages:
            # get message details
            msg = service.users().messages().get(userId=user, id=m['id'], format="full").execute()
            print(msg['snippet'])

            # print the subject
            headers=msg["payload"]["headers"]
            subject= [i['value'] for i in headers if i["name"]=="Subject"]
            print(subject)

            s = getSender(msg)
            print(s)

            msgs.append(msg)

        return msgs

def getSubject(msg):
    "Returns subject from given message"

    return getHeaderInfo(msg, 'Subject')
    # headers=msg["payload"]["headers"]
    # subject= [i['value'] for i in headers if i["name"]=="Subject"]
    # assert len(subject) < 2
    # if len(subject) > 0:
    #     return subject[0]
    # else:
    #     return None

def getSender(msg):
    return getHeaderInfo(msg, 'From')

def getHeaderInfo(msg, infoType):
    "Returns subject from given message"

    headers=msg["payload"]["headers"]
    subject= [i['value'] for i in headers if i["name"]==infoType]
    assert len(subject) < 2
    if len(subject) > 0:
        return subject[0]
    else:
        return None

def readSpecialEmails(subj, sender, markAsRead=True):
    "Gets unread emails, and marks special ones as read"
    msgs = getUnReadMessages()
    msgs = [m for m in msgs if getSubject(m) == subj and getSender(m) == sender]
    print("found %d special messages" % len(msgs))

    # mark each of these as read
    if markAsRead:
        userId = 'me'
        service = getService()
        for msg in msgs:
            # This will mark the messagea as read
            service.users().messages().modify(userId=userId, id=msg['id'],body={ 'removeLabelIds': ['UNREAD']}).execute() 

def testSendMessage():
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         creds = pickle.load(token)

    # service = build('gmail', 'v1', credentials=creds)

    service = getService()
    me = "paulmarganian@gmail.com"
    # msg = create_message(me, me, "test", "test text")
    fn = "robotPic1.jpg"
    msg = create_message_with_attachment(me, me, "test", "test text", fn)
    send_message(service, 'me', msg)

def main():
    
    from settings import SUBJ, SENDER
    readSpecialEmails(SUBJ, SENDER)

if __name__ == "__main__":
    main()