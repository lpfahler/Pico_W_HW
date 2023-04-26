# Program to use PWM to control brightness of an LED
# HW for Lesson 9
# Lori Pfahler
# April 2023


# import modules
from machine import Pin, PWM
from utime import sleep

# function to scale x to y based on range of x and y
def scale(value, x1, x2, y1, y2):
    slope = (y2 - y1)/(x2 - x1)
    scaled_value = slope * (value - x1) + y1
    return(scaled_value)

# setup redLED with PWM
redLED_PWM = PWM(Pin(13))
redLED_PWM.freq(1000)
redLED_PWM.duty_u16(0)

try:
    while True:
        userRequest = float(input("What Voltage Would You Like for the LED? "))
        request16bit = scale(userRequest, 0, 3.3, 0, 65535)
        redLED_PWM.duty_u16(int(request16bit))
        print(int(request16bit))
        sleep(1)
        
except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)
