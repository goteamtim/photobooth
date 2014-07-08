import time
import picamera
import pygame
import sys
import os

capturedImageFileNames = []

now = time.strftime("%H%M%S")
day = time.strftime("%d%m%y")

x = int(raw_input("Enter 1 if you love America! "))

if x==1:

        # INIT CAMERA
        camera = picamera.PiCamera()
        
        camera.vflip = True
        camera.hflip = False
        camera.brightness = 60
        camera.resolution = (612,612)
        #camera.start_preview()
        
        #time.sleep(0.5)
        #camera.capture('image.jpeg', format='jpeg')
        #camera.stop_preview()

        if not os.path.exists("/home/pi/photobooth/"+day): #If the folder for today does not exist create it
                os.makedirs("/home/pi/photobooth/"+day)
        
        camera.capture('/home/pi/photobooth/%s/image%s.jpeg'% (day, now)) #save in the today folder with current time
        camera.close()
        print 'Your photo has been taken.'
        sys.exit(0)

else :
	print "Thank you, no photos taken."
	exit()

sys.exit(0)
