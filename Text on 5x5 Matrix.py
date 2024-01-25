# Lesson 53 McWhorter's Pico W Course
# Text with 5x5 NeoPixel Matrix
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
    'PINK'             : (255, 20, 147),
    'INDIGO'           : (75, 0, 130),
    'BLACK'            : (0, 0, 0),   
    }

# create a brightness function to adjusted rgb codes
def brightness(color_rgb, level = 0.2):
    adj_rgb = tuple(int(code * level) for code in color_rgb)
    return adj_rgb

# create a clear neopixel object function
def clear(neo_object):
     neo_object.fill(colors['BLACK'])       
     neo_object.write()

letters = {
    'L' : [15, 16, 17, 18, 19, 10, 9, 0],
    'O' : [15, 16, 17, 18, 19, 10, 9, 0, 1, 2, 3, 4, 5, 14],
    'R' : [15, 16, 17, 18, 19, 14, 5, 4, 3, 2, 7, 12, 8, 0],
    'I' : [15, 14, 5, 13, 12, 11, 10, 19, 9],
    }

delayTime = 0.5

try:
    while True:        
        # clear matrix
        clear(myMatrix)
        
        # L
        for pixel in letters['L']:
            myMatrix[pixel] = brightness(colors['INDIGO'], level = 0.1)
        myMatrix.write()
        sleep(delayTime)

        # clear matrix
        clear(myMatrix)
        
        # O
        for pixel in letters['O']:
            myMatrix[pixel] = brightness(colors['INDIGO'], level = 0.1)
        myMatrix.write()
        sleep(delayTime)
        
        # clear matrix
        clear(myMatrix)
        
        # R
        for pixel in letters['R']:
            myMatrix[pixel] = brightness(colors['INDIGO'], level = 0.1)
        myMatrix.write()
        sleep(delayTime)
        
        # clear matrix
        clear(myMatrix)
        
        # I
        for pixel in letters['I']:
            myMatrix[pixel] = brightness(colors['INDIGO'], level = 0.1)
        myMatrix.write()
        sleep(delayTime)

        
except KeyboardInterrupt:
    # turn matrix off
    clear(myMatrix)    
     
