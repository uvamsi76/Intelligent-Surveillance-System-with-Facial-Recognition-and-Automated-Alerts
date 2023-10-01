import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client
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
def send_email():
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

def capture_video():
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


#*************************************************** fACE RECOGNITION **************************************************************************
def fr(path):
    print('processing started')
    print()
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    out=cv2.VideoWriter(filepath+'Test1.mp4',fourcc,15.0,(640,480))
    file_video_stream = cv2.VideoCapture(path)
    vamsi_image = face_recognition.load_image_file('/home/pi/Desktop/sample/vamsi.jpg')
    vamsi_face_encodings = face_recognition.face_encodings(vamsi_image)[0]
    kethan_image = face_recognition.load_image_file('/home/pi/Desktop/sample/kethan.jpg')
    kethan_face_encodings = face_recognition.face_encodings(kethan_image)[0]
    sarva_image = face_recognition.load_image_file('/home/pi/Desktop/sample/sarva.jpg')
    sarva_face_encodings = face_recognition.face_encodings(sarva_image)[0]

    hrithik_image = face_recognition.load_image_file('/home/pi/Desktop/sample/hrithik.jpg')
    hrithik_face_encodings = face_recognition.face_encodings(hrithik_image)[0]
    '''
    abhi_image = face_recognition.load_image_file('images/samples/abhi.jpg')
    abhi_face_encodings = face_recognition.face_encodings(abhi_image)[0]
    '''
    known_face_encodings = [vamsi_face_encodings,kethan_face_encodings,sarva_face_encodings,hrithik_face_encodings]
    known_face_names = ["vamsi","kethan","sarva","hrithik"]
    all_face_locations = []
    all_face_encodings = []
    all_face_names = []
    global st
    while (file_video_stream.isOpened):
        ret,current_frame = file_video_stream.read()
        current_frame_small = cv2.resize(current_frame,(0,0),fx=0.25,fy=0.25)
        all_face_locations = face_recognition.face_locations(current_frame_small,number_of_times_to_upsample=1,model='hog')
        

        all_face_encodings = face_recognition.face_encodings(current_frame_small,all_face_locations)

        for current_face_location,current_face_encoding in zip(all_face_locations,all_face_encodings):
            top_pos,right_pos,bottom_pos,left_pos = current_face_location
            
            top_pos = top_pos*4
            right_pos = right_pos*4
            bottom_pos = bottom_pos*4
            left_pos = left_pos*4
            
            all_matches = face_recognition.compare_faces(known_face_encodings, current_face_encoding)
           
            name_of_person = 'Unknown face'
            
            if True in all_matches:
                first_match_index = all_matches.index(True)
                name_of_person = known_face_names[first_match_index]
                st=1
                break

            if(st==1):
                break
            cv2.rectangle(current_frame,(left_pos,top_pos),(right_pos,bottom_pos),(255,0,0),2)
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(current_frame, name_of_person, (left_pos,bottom_pos), font, 0.5, (255,255,255),1)
        
        #cv2.imshow("Webcam Video",current_frame)
        if(st==1):
            break
        if(ret==True and st==0):
            out.write(current_frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    file_video_stream.release()
    cv2.destroyAllWindows()
def buzzer(st):
    if(st):
        GPIO.output(17,GPIO.HIGH)
        time.sleep(1)
        GPIO.output(17,GPIO.LOW)
    else:
        for i in range(15):
            GPIO.output(17,GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(17,GPIO.LOW)
            time.sleep(0.2)
    GPIO.cleanup()
#*************************************************** Main code for method call ********************************************************************

st=0
print('started!!!!')
while True:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    if GPIO.input(4):
        print("Motion Detected")
        print()
        time.sleep(2)
        capture_video()
        time.sleep(2)
        try:
            fr(path)
        except Exception as e:
            print(e)
            pass
        time.sleep(2)
        #buzzer(st)
        if(st==0):
            call()
            send_email()
        else:
            print('face recognised no email required!   :)')
        time.sleep(2)
        #i=0
    #else:
        #break
