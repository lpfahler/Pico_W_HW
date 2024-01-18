# Lesson 53 McWhorter's Pico W Course
# Move Left or Right
# Lori Pfahler
# January 2024

# import modules - using neopixel library that is built in
import neopixel
from machine import Pin
from utime import sleep, sleep_ms

# setup neopixel string
strPin = 0
nPixels = 8
myString = neopixel.NeoPixel(Pin(strPin), nPixels)

# setup potentiometer to control speed of scanning
myPot = machine.ADC(26)

# delay times
fastDelay = 0.01
slowDelay = 0.2
# slope for equation to link delayTime to potValue
slope = (slowDelay - fastDelay)/65535

# color dictionary
colors = {
    'RED'              : (255, 0, 0),
    'GREEN'            : (0, 255, 0),
    'BLUE'             : (0, 0, 255),
    'CYAN'             : (0, 255, 5),
    'MAGENTA'          : (255, 0, 255),
    'YELLOW'           : (255, 255, 0),
    'ORANGE'           : (255, 128, 0),
    'WHITE'            : (255, 255, 255),
    'BLACK'            : (0, 0, 0),   
    }


def move_right(pixelStr, lenStr, step):
    ''' Move colors on neopixel string to the right by the number
        of steps provided.  The pixel at index 0 is the leftmost pixel.
        The colors will 'Loop' around.
    '''
    # preserve the current colors of the pixelStr
    current_colors = []
    for i in range(0, lenStr):
        current_colors.append(pixelStr[i])
    # move the colors by step to the right
    new_colors = current_colors[-step:] + current_colors[:-step]
    for i in range(0, lenStr):
        pixelStr[i] = new_colors[i]
    myString.write()


def move_left(pixelStr, lenStr, step):
    ''' Move colors on neopixel string to the left by the number
        of steps provided.  The pixel at index 0 is the leftmost pixel.
        The colors will 'Loop' around.
    '''
    # preserve the current colors of the pixelStr
    current_colors = []
    for i in range(0, lenStr):
        current_colors.append(pixelStr[i])
    # move the colors by step to the left
    new_colors = current_colors[step:] + current_colors[:step]
    for i in range(0, lenStr):
        pixelStr[i] = new_colors[i]
    myString.write()


# set initial string colors
myString[0] = colors['ORANGE']
myString[1] = colors['MAGENTA']
myString[2] = colors['YELLOW']

try:
    while True:
        potValue = myPot.read_u16()
        # scale the potValue to the desired range of delay times
        delayTime = (slope * potValue) + fastDelay
        # print for debugging and observing potValue and delayTime
        print(f'potValue: {potValue:5d}, delayTime: {delayTime:4.2f}', end = '\r')
        # move_right(myString, nPixels, step = 1)
        move_left(myString, nPixels, step = 1)
        sleep(delayTime)

except KeyboardInterrupt:
    myString.fill(colors['BLACK'])
    myString.write()


    



