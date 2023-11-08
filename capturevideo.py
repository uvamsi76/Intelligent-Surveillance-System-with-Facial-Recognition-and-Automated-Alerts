import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client

def capture_video(filepath):
    print('capturing video')
    print()
    cap=cv2.VideoCapture(0)

    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    out=cv2.VideoWriter(filepath+'Test.mp4',fourcc,10.0,(640,480))
    t0=time.time()
    while(cap.isOpened()):
        ret,frame=cap.read()
        if(ret==True):
            #frame=cv2.flip(frame,0)
            out.write(frame)
            t1=time.time()
            if(cv2.waitKey(1) & int(t1-t0)==10):
                break
        else:
            break
    print('capture done!!!')
    print()
    cap.release()
    cv2.destroyAllWindows()

