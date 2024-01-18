# Lesson 53 McWhorter's Pico W Course
# Fade In and Out
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
    'RED_255'          : (255, 0 ,0),
    'RED_128'          : (128, 0, 0),
    'RED_50'           : (50, 0, 0),
    'RED_25'           : (25, 0, 0),
    'RED_10'           : (10, 0, 0),
    'RED_5'            : (5, 0, 0),
    'RED_1'            : (1, 0, 0),
    'GREEN_255'        : (0, 255, 0),
    'GREEN_128'        : (0, 128, 0),
    'GREEN_50'         : (0, 50, 0),
    'GREEN_25'         : (0, 25, 0),
    'GREEN_10'         : (0, 10, 0),
    'GREEN_5'          : (0, 5, 0),
    'GREEN_1'          : (0, 1, 0),
    'BLUE_255'         : (0, 0, 255),
    'BLUE_128'         : (0, 0, 128),
    'BLUE_50'          : (0, 0, 50),
    'BLUE_25'          : (0, 0, 25),
    'BLUE_10'          : (0, 0, 10),
    'BLUE_5'           : (0, 0, 5),
    'BLUE_1'           : (0, 0, 1),
    'BLACK'            : (0, 0, 0),   
    }

# create the fade list of length 7
red_list = [colors['RED_255'], colors['RED_128'], colors['RED_50'], colors['RED_25'],
            colors['RED_10'], colors['RED_5'], colors['RED_1'], colors['BLACK']]

green_list = [colors['GREEN_255'], colors['GREEN_128'], colors['GREEN_50'], colors['GREEN_25'],
            colors['GREEN_10'],colors['GREEN_5'], colors['GREEN_1'], colors['BLACK']]

blue_list = [colors['BLUE_255'], colors['BLUE_128'], colors['BLUE_50'], colors['BLUE_25'],
            colors['BLUE_10'],colors['BLUE_5'], colors['BLUE_1'], colors['BLACK']]

# number of shades of the colors lists
lenColor = 8

# select the color to use
colorChoice = input('Enter color choice (red, green, blue): ').lower()

try:
    while True:
        for i in range(0, lenColor):
            potValue = myPot.read_u16()
            # scale the potValue to the desired range of delay times
            delayTime = (slope * potValue) + fastDelay
            # print for debugging and observing potValue and delayTime
            print(f'potValue: {potValue:5d}, delayTime: {delayTime:4.2f}', end = '\r')
            if colorChoice == 'blue':
                myString[0] = blue_list[(i + 3) % 7]
                myString[1] = blue_list[(i + 2) % 7]
                myString[2] = blue_list[(i + 1) % 7]
                myString[3] = blue_list[i % 7]
                myString[4] = blue_list[i % 7]
                myString[5] = blue_list[(i + 1) % 7]
                myString[6] = blue_list[(i + 2) % 7]
                myString[7] = blue_list[(i + 3) % 7]
            if colorChoice == 'green':
                myString[0] = green_list[(i + 3) % 7]
                myString[1] = green_list[(i + 2) % 7]
                myString[2] = green_list[(i + 1) % 7]
                myString[3] = green_list[i % 7]
                myString[4] = green_list[i % 7]
                myString[5] = green_list[(i + 1) % 7]
                myString[6] = green_list[(i + 2) % 7]
                myString[7] = green_list[(i + 3) % 7]
            if colorChoice == 'red':
                myString[0] = red_list[(i + 3) % 7]
                myString[1] = red_list[(i + 2) % 7]
                myString[2] = red_list[(i + 1) % 7]
                myString[3] = red_list[i % 7]
                myString[4] = red_list[i % 7]
                myString[5] = red_list[(i + 1) % 7]
                myString[6] = red_list[(i + 2) % 7]
                myString[7] = red_list[(i + 3) % 7]
            myString.write()
            sleep(delayTime)
            

except KeyboardInterrupt:
    myString.fill(colors['BLACK'])
    myString.write()


    




