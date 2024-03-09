# Lesson 59/60 McWhorter's Pico W Course
# Using a Joystick - return angle -
# Light neopixel with appropriate color for that position on the color wheel
# If you press the button on the joystick, show currentn color wheel value on ring
# Lori Pfahler
# March 2024


# import modules
from machine import Pin, ADC
from utime import sleep, ticks_ms, ticks_diff
from math import atan2, pi, sqrt
# download neopixel.py to pico w
from neopixel import Neopixel

# setup Neopixel ring
ring = Neopixel(24, 1, 18, "GRBW")
ring.brightness(5)
ring.fill(rgb_w = (0, 0, 0))
ring.show()

# setup joystick
xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
button = Pin(12,Pin.IN, Pin.PULL_UP)

# variables to track interrupt activation and time for debouncing
interrupt_flag = 0
debounce_time = ticks_ms()

# interrupt function
def button_handler(button):
    global interrupt_flag, debounce_time
    if ticks_diff(ticks_ms(), debounce_time) > 300:
        interrupt_flag = 1
        debounce_time=ticks_ms()

# interrupt request
button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)


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
    curColor = hue2rgb(angle)
    neopixelObject.set_pixel(curPixel, rgb_w = curColor)
    neopixelObject.show()

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
        if distOrigin < 15:
            # avoid calculating an angle for joystick when it is "at rest"
            angleDegrees = 0    
        elif yUnit > 0:
            # use atan2() to get result between -pi and pi
            angleRadians = atan2(yUnit, xUnit)
            angleDegrees = angleRadians * (180 / pi)
        else:
            angleRadians = atan2(yUnit, xUnit)
            angleDegrees = 360 + (angleRadians * (180 / pi))
        anglePixel(angleDegrees, ring)
        if interrupt_flag == 1:
            interrupt_flag = 0
            ring.fill(rgb_w = hue2rgb(angleDegrees))
            ring.show()
            sleep(0.5)
        print(f"X: {xUnit:>6.1f}, Y: {yUnit:>6.1f}, angle deg: {angleDegrees:>3.0f} degrees", end = '\r')
        sleep(0.05)
    
except KeyboardInterrupt:
    ring.fill(rgb_w = (0, 0, 0))
    ring.show()


