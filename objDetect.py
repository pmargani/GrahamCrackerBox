import os

import cv2

VIRTUAL_ENV = 'VIRTUAL_ENV'

VENV_PATH = os.environ[VIRTUAL_ENV] if VIRTUAL_ENV in os.environ else None

def detectObj(imgFile, xmlFile, scale=None, minN=None):

    cascade = cv2.CascadeClassifier(xmlFile)

    img = cv2.imread(imgFile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if scale is None:
        scale = 1.3
    
    if minN is None:
        minN = 5

    rects = cascade.detectMultiScale(gray, scale, minN)

    return rects

def detectFace(imgFile):

    
    xmlPath = "lib/python3.8/site-packages/cv2/data/"
    faceXml = 'haarcascade_frontalface_default.xml'	
    xmlFile = os.path.join(VENV_PATH, xmlPath, faceXml)
    assert os.path.isfile(xmlFile)

    return detectObj(imgFile, xmlFile)

def testDetectFace(fn):
    # fn = "face.jpg"

    faces = detectFace(fn)

    img = cv2.imread(fn)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)       

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()        

def main():
	testDetectFace('face.jgp')

if __name__ == '__main__':
	main()
