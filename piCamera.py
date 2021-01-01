import time

from picamera import PiCamera

from objDetect import detectFace
from gmail import readSpecialEmails, getService, send_message, create_message_with_attachment
from settings import SUBJ, SENDER, FROM

def captureImage(fn=None):

    if fn is None:
        fn = "image.jpg"

    c = PiCamera()
    
    # settings
    c.rotation = 180
    c.resolution = (500, 450) #(1920, 1080)

    # take a picture and save it
    c.capture(fn)

def sendImage(fn, faceDetected=False):

    service = getService()
    subj = SUBJ + " reply"
    txt = "Face Detected: " + str(faceDetected)
    msg = create_message_with_attachment(FROM, FROM, subj, txt, fn)
    send_message(service, FROM, msg)

def emailImage(faceDetect=True):

    # is it time to take an image?
    msgs = readSpecialEmails(SUBJ, SENDER)

    if msgs:
        # yes; take picture
        fn = "image.jpg"
        captureImage(fn)
        
        # look for a face?
        faceDetected = False
        if faceDetect:
            rects = detectFace(fn)
            faceDetected = len(rects) > 0
        
        # and send it
        sendImage(fn, faceDetected)
        print("Sent message with image!")

def main():
    print("piCamera.py")
    emailImage()
    #captureImage("test.jpg")

if __name__ == '__main__':
    main()
