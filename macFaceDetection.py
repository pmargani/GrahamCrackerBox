import os

import cv2

from objDetect import detectFace, testDetectFace


def macTakeImage(captureFn):


    # cv2.namedWindow("preview")
    # vc = cv2.VideoCapture(0)

    # rval = False
    # frame = None

    # if vc.isOpened(): # try to get the first frame
    #     rval, frame = vc.read()

    # return rval, frame

    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite(captureFn, frame)
            break

    cap.release()
    cv2.destroyAllWindows()

def macFaceDetection():

    # take image with mac web came
    fn = 'capture.jpg'
    macTakeImage(fn)
    assert os.path.isfile(fn)

    # look for face
    testDetectFace(fn)

def main():
    macFaceDetection()

if __name__ == '__main__':
    main()