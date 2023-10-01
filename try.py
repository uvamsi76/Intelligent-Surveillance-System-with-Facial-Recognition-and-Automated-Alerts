import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
i=0
while(i!=5):
    if(GPIO.input(4)):
        print('yes')
    else:
        print('no')
    i+=1
    time.sleep(2)