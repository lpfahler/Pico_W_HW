# Program to use a potentiometer
# as a dimmer switch for an LED 
# HW for Pico Lesson 10 and 11
# Lori Pfahler
# April 2023


# import modules
from machine import Pin, PWM
from utime import sleep

# setup potentiometers on ADC pins: ADC0 and ADC1
myPot = machine.ADC(26)

# setup redLED with PWM
redLED_PWM = PWM(Pin(13))
redLED_PWM.freq(1000)
redLED_PWM.duty_u16(0)

try:
    while True:
        potValue = myPot.read_u16()
        if potValue < 700:
            potValue = 0
        if potValue > 65500:
            potValue = 65535
        redLED_PWM.duty_u16(int(potValue))
        print(potValue)
        sleep(0.2)
        
except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)

    

