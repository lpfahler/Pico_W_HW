# Program for RGB LED Dimmer Using Potentiometers for Lesson 13
# with nonlinear dimming equation
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
        # clean up the pot readings or use nonlinear dimming equation
        if redValue < 700:
            red16bit = 0
        elif redValue > 65500:
            red16bit = 65535
        else:
            # equation using a range 0-4095 scale
            # put redValue on 0-4095 scale (use percent of redValue)
            redVal4095 = (redValue/65535)*4095
            redEQ4095 = 4095**(redVal4095/4095)
            # scale input to duty_u16() function back to 0-65535 16bit scale 
            red16bit = (redEQ4095/4095)*65535
            
        if greenValue < 700:
            green16bit = 0
        elif greenValue > 65500:
            green16bit = 65535
        else:
            # equation using a range 0-4095 scale
            # put greenValue on 0-4095 scale (use percent of greenValue)
            greenVal4095 = (greenValue/65535)*4095
            greenEQ4095 = 4095**(greenVal4095/4095)
            # scale input to duty_u16() function back to 0-65535 16bit scale 
            green16bit = (greenEQ4095/4095)*65535
            
        if blueValue < 700:
            blue16bit = 0
        elif blueValue > 65500:
            blue16bit = 65535
        else:
            # equation using a range 0-4095 scale
            # put blueValue on 0-4095 scale (use percent of blueValue)
            blueVal4095 = (blueValue/65535)*4095
            blueEQ4095 = 4095**(blueVal4095/4095)
            # scale input to duty_u16() function back to 0-65535 16bit scale 
            blue16bit = (blueEQ4095/4095)*65535   
        
        # light the RGB LED
        redLED_PWM.duty_u16(int(red16bit))
        greenLED_PWM.duty_u16(int(green16bit))
        blueLED_PWM.duty_u16(int(blue16bit))
        # print out the results
        print(f'red = {int(red16bit):>5}, green = {int(green16bit):>5}, blue = {int(blue16bit):>5}', end = '\r')
        sleep(0.01)    
    


except KeyboardInterrupt:
    redLED_PWM.duty_u16(0)
    greenLED_PWM.duty_u16(0)
    blueLED_PWM.duty_u16(0)