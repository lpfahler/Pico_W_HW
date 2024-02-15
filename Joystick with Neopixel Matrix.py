# Lesson 56 McWhorter's Pico W Course
# Using a Joystick
# Lori Pfahler
# February 2024

# import modules - using neopixel library that is built in
import neopixel
from machine import Pin, ADC
from utime import sleep
# color dictionary in a separate file
from color_dict import colors
from random import choice

# setup neopixel matrix
nPixels = 25
myMatrix = neopixel.NeoPixel(Pin(16), nPixels)

# setup joystick
xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
button = Pin(8,Pin.IN, Pin.PULL_UP)

# create a brightness function to adjusted rgb codes
def brightness(color_rgb, level = 0.2):
    adj_rgb = tuple(int(code * level) for code in color_rgb)
    return adj_rgb

# create a clear neopixel object function
def clear(neo_object):
     neo_object.fill(colors['BLACK'])       
     neo_object.write()
     
def mapRange(value, xLow, xHigh, yLow, yHigh):
    '''Linerly map a value in x range to the y range, similar to map function for Arduino'''
    slope = (yHigh - yLow)/(xHigh - xLow)
    newValue = slope * (value - xLow) + yLow
    return newValue

#  GRID TO PIXEL NUMBER LAYOUT FOR NEOPIXEL MATRIX
#
#           ~350 = 0               ~65535 = 4
#                  0   1   2   3   4 <-- YAxis Value after linear map of 350 to 65535
#               |--------------------
#      ~350 = 0 | 24  15  14   5   4
#               |--------------------
#             1 | 23  16  13   6   3
#               |--------------------
#             2 | 22  17  12   7   2
#               |--------------------
#             3 | 21  18  11   8   1
#               |--------------------
#    ~65535 = 4 | 20  19  10   9   0
#
#             ^
#             |
#             XAxis Value after linear map of 350 to 65535

# dictionary to link grid values to pixel number
matrix_dict = {
    (0,0) : 24,    (0,1) : 15,    (0,2) : 14,    (0,3) : 5,    (0,4) : 4,
    (1,0) : 23,    (1,1) : 16,    (1,2) : 13,    (1,3) : 6,    (1,4) : 3,
    (2,0) : 22,    (2,1) : 17,    (2,2) : 12,    (2,3) : 7,    (2,4) : 2,
    (3,0) : 21,    (3,1) : 18,    (3,2) : 11,    (3,3) : 8,    (3,4) : 1,
    (4,0) : 20,    (4,1) : 19,    (4,2) : 10,    (4,3) : 9,    (4,4) : 0,
}

# set initial pixel location
xGridPrevious = 2
yGridPrevious = 2

# set initial pixel color
new_color = 'BLUE'

try:
    while True:
        # read the x and y potentiometers
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
            
        # determine the grid location on neopixel matrix to illuminate
        xGrid = int(mapRange(xValue, xLow = 500, xHigh = 65535, yLow = 0, yHigh = 4))
        yGrid = int(mapRange(yValue, xLow = 500, xHigh = 65535, yLow = 0, yHigh = 4))
        
        # read buttonValue
        buttonValue = button.value()
        
        # get a new color if user presses button
        if buttonValue == 0:
            new_color = choice(list(colors))
        
        # clear the display
        clear(myMatrix)
        
        # turn on appropriate pixel
        curr_pixel = matrix_dict[(xGrid, yGrid)]           
        myMatrix[curr_pixel] = brightness(colors[new_color], level = 0.1)
        myMatrix.write()
          
        sleep(0.1)
        print(f"X: {xValue:5d}, xGrid: {xGrid:2d}, Y: {yValue:5d} yGrid: {yGrid:2d}", end = '\r')

except KeyboardInterrupt:
    # clear the matrix
    clear(myMatrix)
