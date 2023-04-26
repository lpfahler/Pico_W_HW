# Program to use a potentiometer
# as a dimmer switch for an LED
# comparing various nonlinear scalings for dimming
# HW for Pico Lesson 10 and 11
# Lori Pfahler
# April 2023


# import modules
from machine import Pin, PWM, ADC
from utime import sleep

# setup potentiometers on ADC pins: ADC0 and ADC1
myPot = machine.ADC(26)

# setup red LEDs with PWM
# eq65535 LED
red1LED_PWM = PWM(Pin(13))
red1LED_PWM.freq(1000)
red1LED_PWM.duty_u16(0)
# eq4095 LED
red2LED_PWM = PWM(Pin(14))
red2LED_PWM.freq(1000)
red2LED_PWM.duty_u16(0)
# eq100 LED
red3LED_PWM = PWM(Pin(11))
red3LED_PWM.freq(1000)
red3LED_PWM.duty_u16(0)

# setting of the potentiometer - 0%, 5%, 10%, 50%, 75%, and 100%
potList = [0, 3277, 6554, 32768, 49151, 65535]

try:
    while True:
        for i in potList:
            potValue = i
            # equation from lesson 11
            eq65535 = 65535**(potValue/65535)
            # equation using a range 0-4095 - simulating getting a 12 bit result
            # put potValue on 0-4095 scale (use percent of potValue)
            potVal4095 = (potValue/65535)*4095
            eq4095 = 4095**(potVal4095/4095)
            # equation using a range 0-100
            # put potValue on 0-100 scale (use percent of potValue)
            potVal100 = (potValue/65535)*100
            eq100 = 100**(potVal100/100)
            # scale input to duty_u16() function back to 0-65535 scale 
            eq4095_scaled = (eq4095/4095)*65535
            eq100_scaled = (eq100/100)*65535
            potValue_percent = potValue/65535*100
            print(f"{potValue_percent:>3.1f}%, potValue ={potValue:>5}, eq65535 ={int(eq65535):>5}, eq4095 ={int(eq4095_scaled):>5}, eq100 ={int(eq100_scaled):>5}", end = '\r')
            # light the LEDs
            red1LED_PWM.duty_u16(int(eq65535))
            red2LED_PWM.duty_u16(int(eq4095_scaled))
            red3LED_PWM.duty_u16(int(eq100_scaled))
            sleep(4)
            
except KeyboardInterrupt:
    # turn off LEDs
    red1LED_PWM.duty_u16(0)
    red2LED_PWM.duty_u16(0)
    red3LED_PWM.duty_u16(0)
        


