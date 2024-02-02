# Lesson 54 McWhorter's Pico W Course
# Advanced Rainbow for the String
# Lori Pfahler
# January 2024

# import modules - using neopixel library that is built in
import neopixel
from machine import Pin
from utime import sleep
# new color dictionary in a separate file
from color_dict import colors

# setup neopixel string
strPin = 0
nPixels = 8
myString = neopixel.NeoPixel(Pin(strPin), nPixels)

# setup potentiometer to control speed of scanning
myPot = machine.ADC(26)

# delay times
fastDelay = 0.005
slowDelay = 0.1
# slope for equation to link delayTime to potValue
slope = (slowDelay - fastDelay)/65535

# hue to rgb function; i.e. color wheel to RGB Code
def hue2rgb(deg):
    slope = 255/60
    if deg < 0 or deg > 360:
        deg = deg % 360
    if deg < 60:
        return (255, int(deg * slope), 0)
    elif deg < 120:
        return (int(255 - (deg - 60) * slope), 255, 0)
    elif deg < 180:
        return (0, 255, int((deg - 120) * slope))
    elif deg < 240:
        return (0, int(255 - (deg - 180) * slope), 255)
    elif deg < 300:
        return (int((deg - 240) * slope), 0, 255)
    else:
        return (255, 0, int(255 - (deg - 300) * slope))

# create a brightness function to adjusted rgb codes
def brightness(color_rgb, level = 0.2):
    '''function to adjust rgb codes for desired brightness level
       color_rgb is the code as tuple and level is a value between 0 and 1
       for the brightness'''
    adj_rgb = tuple(int(code * level) for code in color_rgb)
    return adj_rgb

# create a clear neopixel object function
def clear(neo_object):
     neo_object.fill(colors['BLACK'])       
     neo_object.write()
    
# variable to control how much to "stagger" the hue value between pixels
# based on the number of pixels in the string
hue_gap = int(360 / nPixels)

try:
    while True:            
        for hue in range(0, 360):
            # read potentiometer and calculate delay time
            potValue = myPot.read_u16()
            delayTime = (slope * potValue) + fastDelay
            print(f'potValue: {potValue:5d}, delayTime: {delayTime:5.3f}', end = '\r')
            # place the colors on the string
            for pixel in range(0, nPixels):
                myString[pixel] = (brightness(hue2rgb(hue + (hue_gap * pixel)), level = 0.1))                
            myString.write()
            sleep(delayTime)     
     
except KeyboardInterrupt:
    # turn string off
    clear(myString)
    
    