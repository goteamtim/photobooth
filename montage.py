# Import the modules
from PIL import Image, ImageFilter
import time
import os

print "Making your montage..."

filename1 = '1.jpeg'
filename2 = '2.jpeg'
filename3 = '3.jpeg'
filename4 = '4.jpeg'

try:
    # Load an image from the hard drive
    original = Image.open(filename2)

    # Blur the image
    blurred = original.filter(ImageFilter.EDGE_ENHANCE)

    ''' Image filter options
BLUR
CONTOUR
DETAIL
EDGE_ENHANCE,
EDGE_ENHANCE_MORE
EMBOSS
FIND_EDGES
SMOOTH
SMOOTH_MORE
SHARPEN
    '''

    # save the new image
    blurred.save("blurred.png")

except:
    print "Unable to load image"

out = Image.new("RGB", (1269, 1269), "black") #actual final image
'''
Image will be as follows
[1][2]
[3][4]
'''
print "Building..."
out.paste(Image.open("blurred.png"), (int(15), int(15)))# first is x then y
out.paste(Image.open(filename2), (int(642), int(15)))#image number two
out.paste(Image.open(filename3), (int(15), int(642))) #image number three
out.paste(Image.open(filename4), (int(642), int(642))) #image number four

now = time.strftime("%H%M%S")
day = time.strftime("%d%m%y")
print "Saving..."
if not os.path.exists("/home/pi/photobooth/"+day): #If the folder for today does not exist create it
	os.makedirs("/home/pi/photobooth/"+day)
out.save('/home/pi/photobooth/%s/image%s.jpeg'% (day, now)) #save in the today folder with current time

print "Done."
