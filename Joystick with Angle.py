# Lesson 57 McWhorter's Pico W Course
# Using a Joystick - return angle - display on Neopixel ring
# Lori Pfahler
# February 2024


# import modules
from machine import Pin, ADC
from utime import sleep
from math import atan, pi, sqrt
# download neopixel.py to pico w
from neopixel import Neopixel

# setup Neopixel ring
ring = Neopixel(24, 1, 18, "GRBW")
ring.brightness(25)
ring.fill(rgb_w = (0, 0, 0))
ring.show()

# setup joystick
xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
button = Pin(8,Pin.IN, Pin.PULL_UP)

def mapRange(value, xLow, xHigh, yLow, yHigh):
    '''Linearly map a value in x range to the y range, similar to map function for Arduino'''
    slope = (yHigh - yLow)/(xHigh - xLow)
    newValue = slope * (value - xLow) + yLow
    return newValue

def anglePixel(angle, neopixelObject):
    '''light pixel on neopixel ring that corresponds to angle value'''
    neopixelObject.fill(rgb_w = (0, 0, 0))
    # get number of pixels in neopixelObject
    nPixels = neopixelObject.num_leds
    # calculate the number of degrees each pixel will represent
    degPixel = 360/nPixels
    curPixel = (nPixels - int(angle/degPixel)) % nPixels
    neopixelObject.set_pixel(curPixel, rgb_w = (255, 0, 255))
    neopixelObject.show()

try:
    while True:
        # read the x and y potentiometers and button state
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
        # map into -100 to 100 range 
        xUnit = mapRange(xValue, xLow = 350, xHigh = 65535, yLow = -100, yHigh = 100)
        yUnit = mapRange(yValue, xLow = 350, xHigh = 65535, yLow = -100, yHigh = 100)
        # distance from origin
        distOrigin = sqrt(xUnit**2 + yUnit**2)
        # determine angle 
        if distOrigin < 10:
            # avoid calculating an angle for joystick when it is "at rest"
            angleRadians = 0
            angleDegrees = 0    
        elif xUnit < 0 and yUnit > 0:
            angleRadians = atan(yUnit/xUnit)
            angleDegrees = 180 + (angleRadians * (180 / pi))
        elif xUnit < 0 and yUnit < 0:
            angleRadians = atan(yUnit/xUnit)
            angleDegrees = 180 + (angleRadians * (180 / pi))
        elif xUnit > 0 and yUnit < 0:
            angleRadians = atan(yUnit/xUnit)
            angleDegrees = 360 + (angleRadians * (180 / pi))
        else:
            # xUnit > 0 and yUnit > 0
            angleRadians = atan(yUnit/xUnit)
            angleDegrees = angleRadians * (180 / pi)
        anglePixel(angleDegrees, ring)
        print(f"X: {xUnit:>6.1f}, Y: {yUnit:>6.1f}, angle deg: {angleDegrees:>3.0f} degrees", end = '\r')
        sleep(0.1)
    
except KeyboardInterrupt:
    ring.fill(rgb_w = (0, 0, 0))
    ring.show()
