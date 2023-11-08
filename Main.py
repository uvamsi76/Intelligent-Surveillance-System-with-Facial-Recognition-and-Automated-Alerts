import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client
from sendemail import *
from capturevideo import *
from call import * 
from facerecognition import *
from buzzer import *
#*********************************************** GPIO setup *************************************************
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
#*********************************************** Video finename and path *************************************************
filename_part1="surveillance"
file_ext=".mp4"
now = datetime.now()
current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
fname=filename_part1+"_"+current_datetime+file_ext
#filepath="/home/pi/python_code/capture"
filepath="/home/pi/Desktop/test/"
path=filepath+'Test.mp4'

st=0
print('started!!!!')
while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    if GPIO.input(4):
        print("Motion Detected")
        print()
        time.sleep(2)
        capture_video(filepath)
        time.sleep(2)
        try:
            fr(path,filepath)
        except Exception as e:
            print(e)
            pass
        time.sleep(2)
        #buzzer(st)
        if(st==0):
            call()
            send_email(filepath,fname)
        else:
            print('face recognised no email required!   :)')
        time.sleep(2)
        #i=0
    #else:
        #break
