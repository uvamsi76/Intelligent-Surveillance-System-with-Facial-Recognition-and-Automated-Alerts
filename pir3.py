import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
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
st=1
buzzer(st)