import smtplib, os
from email.message import EmailMessage

from datetime import datetime
#import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client
#*********************************************** GPIO setup *************************************************
'''GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)
'''
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


def capture_video():
    global last_frame
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
                last_frame=frame
                break
        else:
            break
    print('capture done!!!')
    cap.release()
    cv2.destroyAllWindows()


def remove_file():
 if os.path.exists("/home/pi/python_code/capture/newvideo.h264"):
  os.remove("/home/pi/python_code/capture/newvideo.h264")
 else:
  print("file does not exist")

 if os.path.exists(filepath+filename):
  os.remove(filepath+filename)
 else:
  print("file does not exist")


#*************************************************** fACE RECOGNITION **************************************************************************
def fr(path):
    global last_frame
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    out=cv2.VideoWriter(filepath+'Test1.mp4',fourcc,20.0,(640,480))
    file_video_stream = cv2.VideoCapture(path)
    vamsi_image = face_recognition.load_image_file('/home/pi/Desktop/sample/vamsi.jpg')
    vamsi_face_encodings = face_recognition.face_encodings(vamsi_image)[0]

    hrithik_image = face_recognition.load_image_file('/home/pi/Desktop/sample/hrithik.jpg')
    hrithik_face_encodings = face_recognition.face_encodings(hrithik_image)[0]
    '''
    abhi_image = face_recognition.load_image_file('images/samples/abhi.jpg')
    abhi_face_encodings = face_recognition.face_encodings(abhi_image)[0]
    '''
    known_face_encodings = [vamsi_face_encodings,hrithik_face_encodings]
    known_face_names = ["vamsi","hrithik"]
    all_face_locations = []
    all_face_encodings = []
    all_face_names = []
    global st
    while (file_video_stream.isOpened):
        ret,current_frame = file_video_stream.read()
        cframe=current_frame
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
                #st=1
                #break

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
        if cv2.waitKey(1) & last_frame==cframe:
            break

    file_video_stream.release()
    cv2.destroyAllWindows()
#*************************************************** Main code for method call ********************************************************************
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
st=0
i=1
last_frame=[]
while True:
 #i = GPIO.input(11)
 if i==1:
  print("Motion Detected")
  capture_video()
  time.sleep(2)
  #res=os.system("MP4Box -add /home/pi/python_code/capture/newvideo.h264 /home/pi/python_code/capture/newvideo.mp4")
  #os.system("mv /home/pi/python_code/capture/newvideo.mp4 "+filepath+filename)
  #os.system("rename C:\\Users\\VAMSI\\Desktop\\test\\Test.mp4 "+filename)
  try:
      fr(path)
  except Exception as e:
      pass
  time.sleep(2)
  '''if(st==0):
      #call()
      send_email()
  else:
      print('face recog no email req')'''
  send_email()
  time.sleep(2)
  #remove_file()
  i=0
 else:
     break
