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

#SETUP GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#FUNCTIONS
def takePicture():
	camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = False
    camera.brightness = 60
    camera.resolution = (612,612)
    if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
            os.makedirs("/home/pi/photoboothPhotos/"+day)
    
    for x in range (0,4):
        temp = '/home/pi/photoboothPhotos/%s/image%s-%s.jpeg'% (day, now,x)
        #camera.image_effect = random.choice(cameraEffectType)
        for p in range(0,3):
                i = 3
                print i-p
                time.sleep(0.5)
        camera.capture(temp) #save in the today folder with current time
        capturedImageFileNames[x] = temp
        #print capturedImageFileNames[x]
        #capturedImageFileNames[x] = temp
    camera.close()
    print 'Your photos have been taken.'
    #sys.exit(0)

GPIO.add_event_detect(23, GPIO.RISING, callback=takePicture, bouncetime=300) #When the button is pressed, it calls the take picture function

capturedImageFileNames = ['','','','']
#cameraEffectType = ['sketch','blur','negative','saturation','posterise','cartoon','pastel']

now = time.strftime("%H%M%S")
day = time.strftime("%d%m%y")

x = int(raw_input("Would you like to take some photos? (yes or no)"))

if string.lower(x)=='yes':
        
        
        # INIT CAMERA
        camera = picamera.PiCamera()
        camera.vflip = True
        camera.hflip = False
        camera.brightness = 60
        camera.resolution = (612,612)

        if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
                os.makedirs("/home/pi/photoboothPhotos/"+day)
        
        for x in range (0,4):
            temp = '/home/pi/photoboothPhotos/%s/image%s-%s.jpeg'% (day, now,x)
            #camera.image_effect = random.choice(cameraEffectType)
            for p in range(0,3):
                    i = 3
                    print i-p
                    time.sleep(0.5)
            camera.capture(temp) #save in the today folder with current time
            capturedImageFileNames[x] = temp
            #print capturedImageFileNames[x]
            #capturedImageFileNames[x] = temp
        camera.close()
        print 'Your photos have been taken.'
        #sys.exit(0)
        

else :
	print "Thank you, no photos taken."
	sys.exit(0)

j = str(raw_input('Would you like to create a montage? (yes or no)'))

if j=='yes':
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
    if not os.path.exists("/home/pi/photoboothPhotos/"+day): #If the folder for today does not exist create it
        os.makedirs("/home/pi/photoboothPhotos/"+day)
    out.save('/home/pi/photoboothPhotos/%s/montage%s.jpeg'% (day, now)) #save in the today folder with current time
	
    print "Done."
    sys.exit(0)

else: 
    sys.exit(0)
