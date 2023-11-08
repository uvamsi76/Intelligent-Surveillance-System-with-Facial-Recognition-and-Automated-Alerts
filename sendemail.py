import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client

def send_email(filepath,fname):
    msg=EmailMessage()
    msg['Subject']='Alert!!!!'
    msg['From']='RPI'
    msg['To']='uvamsi76@gmail.com'
    with open(filepath+'Test1.mp4','rb') as f:
        file_data=f.read()
        msg.add_attachment(file_data,maintype='application',subtype='mp4',filename=fname)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server=smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.login('18r21a04h8@mlrinstitutions.ac.in','MLRIT1234#')
        server.send_message(msg)
    print('Email sent!!!!')
    print()