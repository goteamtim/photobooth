import time
import picamera
import pygame
import sys
import os
from PIL import Image, ImageFilter

capturedImageFileNames = []

now = time.strftime("%H%M%S")
day = time.strftime("%d%m%y")

x = int(raw_input("Enter 1 if you love America! "))

if x==1:
        
        imageFile = '/home/pi/photobooth/%s/image%s.jpeg'% (day, now)
        # INIT CAMERA
        camera = picamera.PiCamera()
        camera.vflip = True
        camera.hflip = False
        camera.brightness = 60
        camera.resolution = (612,612)

        if not os.path.exists("/home/pi/photobooth/"+day): #If the folder for today does not exist create it
                os.makedirs("/home/pi/photobooth/"+day)
        
        for x in range (0,4):
            camera.capture(imageFile) #save in the today folder with current time
            time.sleep(1)
            capturedImageFileNames[x] = imageFile
        camera.close()
        print 'Your photos have been taken.'
        sys.exit()
        

else :
	print "Thank you, no photos taken."
	sys.exit()

j = str(raw_input('Would you like to create a montage? (yes or no)'))

if j=='no':
    sys.exit()
elif j=='yes':
    out = Image.new("RGB", (1269, 1269), "black") #actual final image
    '''
    Image will be as follows
    [1][2]
    [3][4]
    '''
    print "Building..."
    out.paste(Image.open(capturedImageFileNames[0]), (int(15), int(15)))# first is x then y
    out.paste(Image.open(capturedImageFileNames[1]), (int(642), int(15)))#image number two
    out.paste(Image.open(capturedImageFileNames[2]), (int(15), int(642))) #image number three
    out.paste(Image.open(capturedImageFileNames[3]), (int(642), int(642))) #image number four

    print "Saving..."
    if not os.path.exists("/home/pi/photobooth/"+day): #If the folder for today does not exist create it
        os.makedirs("/home/pi/photobooth/"+day)
    out.save('/home/pi/photobooth/%s/montage%s.jpeg'% (day, now)) #save in the today folder with current time

    print "Done."

    sys.exit(0)

else: 
    sys.exit(0)
