# Program to read a potentiometer
# HW for Pico Lesson 5
# Lori Pfahler
# April 2023


# import modules
import machine
from utime import sleep

# setup potentiometers on ADC pins: ADC0 and ADC1
myPot = machine.ADC(28)

# function to scale x to y based on range of x and y
def scale(value, x1, x2, y1, y2):
    slope = (y2 - y1)/(x2 - x1)
    scaled_value = slope * (value - x1) + y1
    return(scaled_value)

while True:
    # read potentiometers
    potValue = myPot.read_u16()
    # read voltage scale
    voltage = scale(potValue, 400, 65535, 0, 3.3)
    # HW challenge scale y1 = 100, y2 = 0 - negative slope
    hwValue = int(scale(potValue, 400, 65535, 100, 0))
    # print values to shell
    print('Voltage Scale:', potValue, '=', voltage) 
    print('Homework Scale:', potValue, '=', hwValue, '\n')
    sleep(1)
    
