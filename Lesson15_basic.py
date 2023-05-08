# Program for Lesson 15 - Basic solution to HW
# RGB LED - show a sequence of colors selected by user
# using one RGB LED
# 
# McWhorter Pico W Course
# Lori Pfahler
# April 2023

# import modules
from machine import Pin, PWM
from utime import sleep

# Setup for RGB LED
redLED = PWM(Pin(15))
redLED.freq(1000)
redLED.duty_u16(0)
greenLED = PWM(Pin(14))
greenLED.freq(1000)
greenLED.duty_u16(0)
blueLED = PWM(Pin(13))
blueLED.freq(1000)
blueLED.duty_u16(0)

# create a dictionary to hold the RGB codes for the colors
colors = {
    1  : (255,   0,   0),
    2  : (  0, 255,   0),
    3  : (  0,   0, 255),
    4  : (  0, 255, 255),
    5  : (255,   0, 255),
    6  : (255, 150,   0),
    7  : (255,  20,   0),
    8  : (255, 255, 255),
    9  : (  0,   0,   0)
    }
      
try:
    while True:
        # Explain to user how to enter the color sequence
        print('Enter a sequence of colors using the assigned number for the color')
        print('separated by a space  e.g. 2 6 8 \n')
        print('1 =red, 2 = green, 3 = blue, 4 = cyan, 5 = magenta')
        print('6 = yellow, 7 = orange, 8 = white, 9 = black \n')
        # figured out this code from stackoverflow.com
        # userColors = [int(x) for x in input('Enter your sequence of colors: ').split()]
        # read in numbers to a list
        colorString = input('Enter your sequence of colors: ')
        colorString = colorString.split()
        userColors = []
        for i in range(0, len(colorString)):
            userColors = userColors + [int(colorString[i])]
        # loop through the requested sequence of colors
        for i in userColors:
            colorRGB = colors.get(i)           
            # light the RGB LEDs - use <<8 to convert to 0-255 to 0-65535 range
            redLED.duty_u16(colorRGB[0]<<8)
            greenLED.duty_u16(colorRGB[1]<<8)
            blueLED.duty_u16(colorRGB[2]<<8)
            sleep (2)
                 
        # turn all off           
        redLED.duty_u16(0)
        greenLED.duty_u16(0)
        blueLED.duty_u16(0)

except KeyboardInterrupt:
    # turn all off
    redLED.duty_u16(0)
    greenLED.duty_u16(0)
    blueLED.duty_u16(0)





