# Program for Lesson 15
# Four RGB LEDs - color sequence chosen by user
# 
# The first RGB LED (RGB 0) will show the current color
# The second RGB LED (RGB 1) will show the previous color after the first loop
# The third and fourth RGB LEDs (RGB 2 and RGB 3) will hold the
# colors two and three loops past from the current color
# 
# McWhorter Pico W Course
# Lori Pfahler
# April 2023

# import modules
from machine import Pin, PWM
from utime import sleep

# pins for RGB LEDs
# RGB 0 is on pins 15, 14, 13
# RGB 1 is on pins 6, 5, 4
# RGB 2 is on pins 9, 8 ,7
# RGB 3 is on pins 12, 11, 10
redPins = [15, 6, 9, 12]
greenPins = [14, 5, 8, 11]
bluePins = [13, 4, 7, 10]

# setup red LEDs
# red
redNames = []
for i in redPins:
    LED_name = 'red'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    redNames.append(LED_name)

#green
greenNames = []
for i in greenPins:
    LED_name = 'green'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    greenNames.append(LED_name)

#blue
blueNames = []
for i in bluePins:
    LED_name = 'blue'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    blueNames.append(LED_name)

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
        # number of colors to go through
        numColors = len(userColors)
        # pad userColors with three leading and trailing black values to make sequence work
        # this way RGB 1, RGB 2 and RGB 3 will be black for the first loop and
        # as needed for second and third loops
        userColors = [9, 9, 9] + userColors + [9, 9, 9]
        # begin loop to run through the colors
        for i in range(0, numColors + 3):
            # the previous colors in the sequence on RGB 1, RGB 2 and RGB 3
            colorRGB3 = colors.get(userColors[i])
            colorRGB2 = colors.get(userColors[i + 1])
            colorRGB1 = colors.get(userColors[i + 2])
            # current color on RGB 0
            colorRGB0 = colors.get(userColors[i + 3])
            
            # light the RGB LEDs
            # current color on RGB 0; use <<8 to convert to 0-255 to 0-65535 range
            redNames[0].duty_u16(colorRGB0[0]<<8)
            greenNames[0].duty_u16(colorRGB0[1]<<8)
            blueNames[0].duty_u16(colorRGB0[2]<<8)
            # previous color on RGB 1
            redNames[1].duty_u16(colorRGB1[0]<<8)
            greenNames[1].duty_u16(colorRGB1[1]<<8)
            blueNames[1].duty_u16(colorRGB1[2]<<8)
            # current color two loops ago on RGB 2
            redNames[2].duty_u16(colorRGB2[0]<<8)
            greenNames[2].duty_u16(colorRGB2[1]<<8)
            blueNames[2].duty_u16(colorRGB2[2]<<8)
            # current color three loops ago on RGB 3
            redNames[3].duty_u16(colorRGB3[0]<<8)
            greenNames[3].duty_u16(colorRGB3[1]<<8)
            blueNames[3].duty_u16(colorRGB3[2]<<8)
            # sleep to hold the color for some time
            sleep (2)
                 
        # turn all off        
        for i in redNames:
            i.duty_u16(0)
        for i in greenNames:
            i.duty_u16(0)
        for i in blueNames:
            i.duty_u16(0)   


except KeyboardInterrupt:
    # turn all off
    for i in redNames:
        i.duty_u16(0)
    for i in greenNames:
        i.duty_u16(0)
    for i in blueNames:
        i.duty_u16(0)





