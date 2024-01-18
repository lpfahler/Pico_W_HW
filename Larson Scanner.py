# Lesson 53 McWhorter's Pico W Course
# Larson Scanner with Potentiometer
# Lori Pfahler
# January 2024

# import modules - using neopixel library that is built in
import neopixel
from machine import Pin
from utime import sleep

# setup neopixel string
strPin = 0
nPixels = 8
myString = neopixel.NeoPixel(Pin(strPin), nPixels)

# setup potentiometer to control speed of scanning
myPot = machine.ADC(26)


# color dictionary
colors = {
    'RED_255'         : (255, 0 ,0),
    'RED_128'         : (128, 0, 0),
    'RED_50'          : (50, 0, 0),
    'RED_5'           : (5, 0, 0),
    'GREEN_255'       : (0, 255, 0),
    'GREEN_128'       : (0, 128, 0),
    'GREEN_50'        : (0, 50, 0),
    'GREEN_5'         : (0, 5, 0),
    'BLACK'           : (0, 0, 0),
    }

# delay times
fastDelay = 0.01
slowDelay = 0.2
# slope for equation to link delayTime to potValue
slope = (slowDelay - fastDelay)/65535

try:
    # [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
    pattern_list = list(range(0, nPixels)) + list(range(nPixels - 2, 0, -1))
    print(pattern_list)
    while True:
        potValue = myPot.read_u16()
        # scale the potValue to the desired range of delay times
        delayTime = (slope * potValue) + fastDelay
        # print for debugging and observing potValue and delayTime
        print(f'potValue: {potValue:5d}, delayTime: {delayTime:4.2f}', end = '\r')
        # create the sequence I want to use for scanner; when nPixels = 8
        for i in pattern_list:

            myString.fill(colors['GREEN_128'])
            myString[i] = colors['RED_128']
            myString.write()
            sleep(delayTime)
            
except KeyboardInterrupt:
    myString.fill(colors['BLACK'])
    myString.write()

