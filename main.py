import httplib2
import pprint
import time
import picamera
#import pygame
import qrcode
from sys import exit
import random
import os
from PIL import Image, ImageFilter
import array
import string
import RPi.GPIO as GPIO

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

#SETUP VARIABLES
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

#Include error handling later
#if not os.path.isfile("/home/totalPictures.dat"): 
        #DataIn = open("/home/totalPictures.dat","w")#Create a writeable file if it doesnt exist
dataIn = open('/home/totalPictures.dat',"r")
totalPicturesTaken = int(dataIn.readline())
dataIn.close()

#SETUP GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#FUNCTIONS
def takePicture(input):
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
    if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
        os.makedirs("/home/pi/photoboothPhotos/"+day)
    out.save('/home/pi/photoboothPhotos/%s/montage%s.jpeg'% (day, now)) #save in the today folder with current time
    print "Picture saved locally, uploading..."
	#writing total pictures amount to local file
	try:
		#uploading to drive
		#Calling out to server and setting total pictures
		break
	except :
		print "Error uploading, file still saved locally."
		
	

GPIO.add_event_detect(23, GPIO.FALLING, callback=takePicture, bouncetime=200) #Button pres calls the take picture function


while True:
    print "Press button one to take a picture and 2 to exit."
    GPIO.wait_for_edge(24, GPIO.FALLING)
    GPIO.Cleanup()
    print "Exiting..."
	f = open('/home/totalPictures.dat',"w")
	f.write(totalPicturesTaken)
	f.close()
    Sys.exit(0)
