# Program to Use Joystick with Pico - just print out values
# Lori Pfahler
# February 2024

from machine import Pin, ADC
from utime import sleep

# setup joystick
xAxis = ADC(Pin(26))
yAxis = ADC(Pin(27))
button = Pin(8,Pin.IN, Pin.PULL_UP)

while True:
    # read the x and y potentiometers and button state
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()
    buttonStatus = "not pressed"
    if buttonValue == 0:
        buttonStatus = "pressed"
    
    print(f"X: {xValue:5d}, Y: {yValue:5d}, button: {buttonValue}, button status: {buttonStatus}")
    sleep(0.2)
    