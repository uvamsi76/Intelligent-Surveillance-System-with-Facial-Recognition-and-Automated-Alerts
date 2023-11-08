import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client

def call():
    acc_sid='AC3d50046bfc67a5d84b8de5e14e1c9dc9'
    auth_token='e6ab67873931c0e18922245d4e3246e8'
    client= Client(acc_sid,auth_token)

    call=client.calls.create(
        twiml='<Response><Say>hello</Say></Response>',
        to='+916300854181',
        from_='+18288822846'
        )
    print('call alert sent!!!!')
    print()