import smtplib, os
from email.message import EmailMessage
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import face_recognition
from twilio.rest import Client
stream=cv2.VideoCapture(0)
def fr(path,filepath):
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