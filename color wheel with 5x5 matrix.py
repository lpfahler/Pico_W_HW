# Lesson 53 McWhorter's Pico W Course
# Use 5x5 NeoPixel Matrix 
# Lori Pfahler
# January 2024

# import modules - using neopixel library that is built in
import neopixel
from machine import Pin
from utime import sleep

# setup neopixel matrix
matrixPin = 16
nPixels = 25
myMatrix = neopixel.NeoPixel(Pin(matrixPin), nPixels)

# setup potentiometer to control speed of scanning
myPot = machine.ADC(26)

# delay times
fastDelay = 0.1
slowDelay = 0.5
# slope for equation to link delayTime to potValue
slope = (slowDelay - fastDelay)/65535

# color dictionary
colors = {
    'RED'              : (255, 0, 0),
    'GREEN'            : (0, 255, 0),
    'BLUE'             : (0, 0, 255),
    'CYAN'             : (0, 255, 255),
    'MAGENTA'          : (255, 0, 255),
    'YELLOW'           : (255, 255, 0),
    'ORANGE'           : (255, 128, 0),
    'WHITE'            : (255, 255, 255),
    'BLACK'            : (0, 0, 0),   
    }


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
    adj_rgb = tuple(int(code * level) for code in color_rgb)
    return adj_rgb

# create a clear neopixel object function
def clear(neo_object):
     neo_object.fill(colors['BLACK'])       
     neo_object.write()
    

# define the outer, inner and middle "squares" for the animation
outer_square = [14, 5, 4, 3, 2, 1, 0, 9, 10, 19, 20, 21, 22, 23, 24, 15]
inner_square = [13, 6, 7, 8, 11, 18, 17, 16]
middle_pixel = 12

try:
    while True:
        # read potentiometer and calculate delay time
        potValue = myPot.read_u16()
        delayTime = (slope * potValue) + fastDelay
        print(f'potValue: {potValue:5d}, delayTime: {delayTime:4.2f}', end = '\r')
        
        # clear matrix
        clear(myMatrix)
        
        # turn on middle pixel
        myMatrix[middle_pixel] = brightness(colors['WHITE'], level = 0.05)
        myMatrix.write()
        
        sleep(delayTime)

        # clear matrix
        clear(myMatrix)
        
        # turn on inner square
        hue = 0
        for pixel in inner_square:
            myMatrix[pixel] = brightness(hue2rgb(hue), level = 0.1)
            hue += 45
        myMatrix.write()
        
        sleep(delayTime)

        # clear matrix
        clear(myMatrix)
        
        # turn on outer square
        hue = 0
        for pixel in outer_square:
            myMatrix[pixel] = brightness(hue2rgb(hue), level = 0.1)
            hue += 23
        myMatrix.write()
       
        sleep(delayTime)
        
        # Go backwards now
        
        # clear matrix
        clear(myMatrix)
        
        # turn on inner square
        hue = 0
        for pixel in inner_square:
            myMatrix[pixel] = brightness(hue2rgb(hue), level = 0.1)
            hue += 45
        myMatrix.write()
        
        sleep(delayTime)
        
except KeyboardInterrupt:
    # turn matrix off
    clear(myMatrix)