import cv2
import face_recognition as fr
from gpiozero import CPUTemperature, LoadAverage
stream=cv2.VideoCapture(0)
fl=[]
while(1):
    r,c=stream.read()
    t=c
    cf=cv2.resize(t,(0,0),fx=1,fy=1)
    fl=fr.face_locations(cf,model='hog')
    for i,cfl in enumerate(fl):
        tp,rt,bt,lf=cfl
        cv2.rectangle(cf,(lf,tp),(rt,bt),(0,0,255),2)
    #cv2.startWindowThread()
    #cv2.namedWindow('stream')
    cv2.imshow("stream",cf)
    #cv2.waitKey(1)
    cpu = CPUTemperature()
    load = LoadAverage()
    cpu_temperature = str((cpu.temperature)//1)
    load_average = str(load.load_average)
    #print (cpu.temperature)
    #print(load.load_average)
    if(float(cpu_temperature)>=60.0):
        break
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
stream.release()
cv2.destroyAllWindows()
