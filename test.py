#!/usr/bin/env python
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
from gpiozero import CPUTemperature, LoadAverage
#Enter credentials for CCTV
rtsp_username = "admin"
rtsp_password = "aswinth347653"
rtsp_IP = "192.168.29.100"
cam_width = 352 #set to resolution of incoming video from DVR
cam_height = 288 #set to resolution of incoming video from DVR
motion_threshold = 1000 #decrease this value to increase sensitivity
cam_no = 1
trig_alarm =0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)
BUZZER = 3
GPIO.setup(BUZZER,GPIO.OUT)
def create_camera (channel):
    rtsp = "rtsp://" + rtsp_username + ":" + rtsp_password + "@" + rtsp_IP + ":554/Streaming/channels/" + channel + "02" #change the IP to suit yours
    #cap = cv2.VideoCapture(rtsp, cv2.CAP_FFMPEG)
    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width)  # ID number for width is 3
    cap.set(4, cam_height)  # ID number for height is 480
    cap.set(10, 100)  # ID number for brightness is 10
    return cap
def read_camera ():
    success, current_screen = cam1.read()
    Main_screen [:cam_height, :cam_width, :3] = current_screen
    #success, current_screen = cam2.read()
    #Main_screen[cam_height:cam_height*2, :cam_width, :3] = current_screen
    #success, current_screen = cam3.read()
    #Main_screen[:cam_height, cam_width:cam_width*2, :3] = current_screen
    #success, current_screen = cam4.read()
    #Main_screen[cam_height:cam_height*2, cam_width:cam_width*2, :3] = current_screen
    return (Main_screen)
def find_screen():
    if (x < cam_width):  
        if (y < cam_height):
            screen = frame1[0:cam_height, 0:cam_width]
            print("Activity in cam screen 1")
        else:
            screen = frame1[cam_height:cam_height*2, :cam_width]
            print("Activity in cam screen 2")
    else:
        if (y < cam_height):
            screen = frame1[:cam_height, cam_width:cam_width*2]
            print("Activity in cam screen 3")
        else:
            screen = frame1[cam_height:cam_height*2, cam_width:cam_width*2]
            print("Activity in cam screen 4")
    return (screen)
#Open all four camera Framers
cam1 = create_camera(str(1))
#cam2 = create_camera(str(2))
#cam3 = create_camera(str(3))
#cam4 = create_camera(str(4))
print ("Reading camera successfull")
Main_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen on which all four camera will be stiched
display_screen = np.zeros(( (cam_height*2), (cam_width*2), 3) , np.uint8) # create screen to be display on 5 inch TFT display
kernal = np.ones((5,5),np.uint8) #form a 5x5 matrix with all ones range is 8-bit
while True:
    frame1 = read_camera() #Read the first frame
    grayImage_F1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Convert to gray
    frame2 = read_camera() #Read the 2nd frame
    grayImage_F2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diffImage = cv2.absdiff(grayImage_F1,grayImage_F2) #get the differance --this is cool
    blurImage = cv2.GaussianBlur(diffImage, (5,5), 0)
    _, thresholdImage = cv2.threshold(blurImage, 20,255,cv2.THRESH_BINARY)
    dilatedImage = cv2.dilate(thresholdImage,kernal,iterations=5)
    #contours, _ = cv2.findContours(dilatedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #find contour is a magic function
    result= cv2.findContours(dilatedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = result if len(result) == 2 else result[1:3]
    for contour in contours: #for every change that is detected
        (x,y,w,h) = cv2.boundingRect(contour) #get the location where change was found
        if cv2.contourArea(contour) > motion_threshold:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 1)
            display_screen = find_screen()
            if ((x>cam_width) and (y<cam_height)): #screen 3
                trig_alarm+=1
            else:
                trig_alarm =0           
    if (trig_alarm>=3):#wait for conts 3 motions 
        #Beep the Buzzer
        GPIO.output(BUZZER,1)
        time.sleep(0.02)
        GPIO.output (BUZZER,0)
        trig_alarm =0
    cpu = CPUTemperature()
    load = LoadAverage()
    cpu_temperature = str((cpu.temperature)//1)
    load_average = str(load.load_average)
    #print (cpu.temperature)
    #print(load.load_average)
    cv2.putText(display_screen, cpu_temperature, (250,250), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
    cv2.putText(display_screen, load_average, (300,250), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 2)
    print(trig_alarm)
    dim = (800, 480)
    Full_frame = cv2.resize (display_screen,dim,interpolation=cv2.INTER_AREA)
    cv2.namedWindow("AISHA", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('AISHA', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("AISHA",Full_frame)
    if cv2.waitKey(1) & 0xFF == ord('p'):
        cam1.release()
        cam2.release()
        cam3.release()
        cam4.release()
        cv2.destroyAllWindows()
        break
