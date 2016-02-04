import time
import picamera
#import pygame
from sys import exit
import random
import os
from PIL import Image, ImageFilter
import array
import string
import RPi.GPIO as GPIO
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

gmuFile = open('/home/pi/id.dat',"r")
secretFile = open('/home/pi/secret.dat',"r")
gmail_user = gmuFile.readline()
gmail_pwd = secretFile.readline()

#Setup total picture count.  
dataIn = open('/home/pi/totalPictures.dat',"r")
totalPicturesTaken = int(dataIn.readline())
print totalPicturesTaken
dataIn.close()

#SETUP GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#FUNCTIONS
def sendMail(to,subject,text,attach):
        msg = MIMEMultipart()
        msg['From']=gmail_user
        msg['To'] = gmail_pwd
        msg['Subject']=subject
        msg.attach(MIMEText(text))

        part = MIMEBase('application','octet-stream')
        part.set_payload(open(attach,'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="%s"' %os.path.basename(attach))
        msg.attach(part)

        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_user,gmail_pwd)
        mailServer.sendmail(gmail_user,to,msg.as_string())
        mailServer.close()

def takePicture(input):
    global totalPicturesTaken
    capturedImageFileNames = ['','','','']
    now = time.strftime("%H%M%S")
    day = time.strftime("%m%d%y")
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = False
    camera.brightness = 60
    camera.resolution = (612,612)
    if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
            os.makedirs("/home/pi/photoboothPhotos/"+day)

    for x in range (0,4):
        temp = '/home/pi/photoboothPhotos/%s/image%s-%s.jpeg'% (day, now,x)
        for p in range(0,3):
                i = 3
                print i-p
                time.sleep(0.5)
        camera.capture(temp) #save in the today folder with current time
        capturedImageFileNames[x] = temp
    camera.close()
    print 'Your photos have been taken, creating montage...'
    out = Image.new("RGB", (1269, 1269), "black") #actual final image
    '''
    Final image will be as follows
    [1][2]
    [3][4]
    '''
    print "Building..."
    out.paste(Image.open(capturedImageFileNames[0]), (int(15), int(15)))# first is x then y
    out.paste(Image.open(capturedImageFileNames[1]), (int(642), int(15)))#image number two
    out.paste(Image.open(capturedImageFileNames[2]), (int(15), int(642))) #image number three
    out.paste(Image.open(capturedImageFileNames[3]), (int(642), int(642))) #image number four
    print "Saving..."
    totalPicturesTaken+=1
    path = '/home/pi/photoboothPhotos/%s/montage%s.jpeg'% (day, now)
    if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
        os.makedirs("/home/pi/photoboothPhotos/"+day)
    out.save(path) #save in the today folder with current time
    print "Picture saved locally, uploading..."
    sendMail("piphotobooth@gmail.com",
             "Image taken!",
             "Email from the photobooth.",
             path)
    print "Done, ready for another picture."
		
GPIO.add_event_detect(23, GPIO.FALLING, callback=takePicture, bouncetime=200) #Button pres calls the take picture function

while True:
    print "Press button one to take a picture and 2 to exit."
    GPIO.wait_for_edge(24, GPIO.FALLING)
    GPIO.cleanup()
    print "Exiting..."
    f = open('/home/pi/totalPictures.dat',"w")
    f.write(str(totalPicturesTaken))
    f.close()
    Sys.exit(0)
