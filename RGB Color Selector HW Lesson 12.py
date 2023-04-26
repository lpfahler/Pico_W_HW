# Program for RGB LED from Lesson 12
# McWhorter Pico W Course
# Lori Pfahler
# April 2023

# import modules
from machine import Pin, PWM
from utime import sleep

# setup red, green and blue for RGB LED
redLED_PWM = PWM(Pin(15))
redLED_PWM.freq(1000 )
redLED_PWM.duty_u16(0)

greenLED_PWM = PWM(Pin(14))
greenLED_PWM.freq(1000)
greenLED_PWM.duty_u16(0)

blueLED_PWM = PWM(Pin(13))
blueLED_PWM.freq(1000)
blueLED_PWM.duty_u16(0)

# create a dictionary to hold the RGB codes for the colors
colors = {
    'red'     : (255,   0,   0),
    'green'   : (  0, 255,   0),
    'blue'    : (  0,   0, 255),
    'cyan'    : (  0, 255, 255),
    'magenta' : (255,   0, 255),
    'yellow'  : (255, 150,   0),
    'orange'  : (255,  20,   0),
    'white'   : (255, 255, 255)
    }
      
try:
    while True:
        userColor = input('Enter red, green, blue, cyan, magenta, yellow, orange, white or RGB: ')
        # find the color in the dictionary - if available
        colorRGB = colors.get(userColor.lower())
        # if userColor was found in the dictionary, do the following
        if colorRGB:
            # use '<<8' to scale the 8bit value (0-255) to 16bit (0-65535)
            redLED_PWM.duty_u16(colorRGB[0]<<8)
            greenLED_PWM.duty_u16(colorRGB[1]<<8)
            blueLED_PWM.duty_u16(colorRGB[2]<<8)
            sleep(1)
        # if the user entered 'RGB', do the following
        elif userColor == 'RGB':
            # get the red, green, blue levels from the user
            print('Enter the RGB code')
            redVal = int(input('Enter the value for red (0-255): '))
            greenVal = int(input('Enter the value for green (0-255): '))
            blueVal = int(input('Enter the value for blue (0-255): '))
            # use '<<8' to scale the 8bit value (0-255) to 16bit (0-65535)
            redLED_PWM.duty_u16(redVal<<8)
            greenLED_PWM.duty_u16(greenVal<<8)
            blueLED_PWM.duty_u16(blueVal<<8)        
            sleep(1)
        # if user entered something that is not in the dictionary or 'RGB', do the following
        else:
            print('Invalid Entry - try again')
            sleep(1)

except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)
    greenLED_PWM.duty_u16(0)
    blueLED_PWM.duty_u16(0)    




