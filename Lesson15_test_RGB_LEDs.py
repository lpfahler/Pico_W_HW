# Program for Lesson 15
# Four RGB LEDs - test code to setup and light four RGBs
# McWhorter Pico W Course
# Lori Pfahler
# April 2023

# import modules
from machine import Pin, PWM
from utime import sleep

# pins for RGB LEDs
redPins = [15, 12, 9, 6]
greenPins = [14, 11, 8, 5]
bluePins = [13, 10, 7, 4]

# setup red LEDs
# red
redNames = []
for i in redPins:
    LED_name = 'red'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    redNames.append(LED_name)
print(redNames)
#green
greenNames = []
for i in greenPins:
    LED_name = 'green'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    greenNames.append(LED_name)
print(greenNames)
#blue
blueNames = []
for i in bluePins:
    LED_name = 'blue'+str(i)
    LED_name = PWM(Pin(i))
    LED_name.freq(1000)
    LED_name.duty_u16(0)
    blueNames.append(LED_name)
print(blueNames)


# turn red on
# use '<<8' to scale the 8bit value (0-255) to 16bit (0-65535)
for i in redNames:
    i.duty_u16(255<<8)
sleep(2)
# turn red off and green on
for i in redNames:
    i.duty_u16(0)
for i in greenNames:
    i.duty_u16(255<<8)
sleep(2)
# turn green off and blue on
for i in greenNames:
    i.duty_u16(0)
for i in blueNames:
    i.duty_u16(255<<8)
sleep(2)

# turn all off
for i in redNames:
    i.duty_u16(0)
for i in greenNames:
    i.duty_u16(0)
for i in blueNames:
    i.duty_u16(0)
