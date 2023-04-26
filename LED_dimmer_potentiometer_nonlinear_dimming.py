# Program to use a potentiometer
# as a dimmer switch for an LED
# with nonlinear scale for dimming
# HW for Pico Lesson 10 and 11
# Lori Pfahler
# April 2023


# import modules
from machine import Pin, PWM, ADC
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
            DC_16bit = 0
        elif potValue > 65500:
            DC_16bit = 65535
        else:
            # equation using a range 0-100
            # put potValue on 0-100 scale (use percent of 16bit potValue)
            potVal100 = (potValue/65535)*100
            eq100 = 100**(potVal100/100)
            # scale input to duty_u16() function back to 0-65535 16bit scale 
            DC_16bit = (eq100/100)*65535
        redLED_PWM.duty_u16(int(DC_16bit))
        sleep(0.1)
        
except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)

    

