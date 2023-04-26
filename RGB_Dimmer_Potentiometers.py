# Program for RGB LED Dimmer Using Potentiometers for Lesson 13
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

# setup potentiometers on ADC pins
redPot = machine.ADC(28)
greenPot = machine.ADC(27)
bluePot = machine.ADC(26)

try:
    while True:
        # read the potentiometers
        redValue = redPot.read_u16()
        greenValue = greenPot.read_u16()
        blueValue = bluePot.read_u16()
        # clean up the pot readings
        if redValue < 700:
            redValue = 0
        if redValue > 65500:
            redValue = 65535
            
        if greenValue < 700:
            greenValue = 0
        if greenValue > 65500:
            greenValue = 65535
            
        if blueValue < 700:
            blueValue = 0
        if blueValue > 65500:
            blueValue = 65535
        # light the RGB LED
        redLED_PWM.duty_u16(int(redValue))
        greenLED_PWM.duty_u16(int(greenValue))
        blueLED_PWM.duty_u16(int(blueValue))
        # print out the results
        print(f'red = {int(redValue):>5}, green = {int(greenValue):>5}, blue = {int(blueValue):>5}', end = '\r')
        sleep(0.01)    
    


except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)
    greenLED_PWM.duty_u16(0)
    blueLED_PWM.duty_u16(0)