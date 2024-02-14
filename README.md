# Intelligent Surveillance System with Facial Recognition and Automated Alerts Using raspberry pi

This is the project where we attached a camera and pir sensor to Raspberrypi and wrote the code in such a way that when ever we detect something in pir sensor the camera starts a 15 sec recording and detects if it has any known faces. If it does not detect any known face then it sends the 15 sec video recording to admins email and calls the admin with an automated message giving a warning sign. 
Flow of it will be  

Activates camera and does face recognition when Motion is detected
If it does no identify face 
It activates buzzer and 
sends video through mail and calls the admin with a warning message


# Tech and Libraries used
    * opencv (for capturing video)
    * Face_recognition (for face recognition)
    * RPi.GPIO (for accessing pins in raspberry pi)
    * smtplib and email.message (for sending the email)
    * twilio.rest (for sending a call)
