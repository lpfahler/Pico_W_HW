# Program to turn an LED on and off with a Button (momentary switch) 
# Lori Pfahler
# May 2023

# import modules
from machine import Pin
import utime

# setup button and LED pins
myButton = Pin(12, Pin.IN, Pin.PULL_UP)
myLED = Pin(15, Pin.OUT)

try:
    while True:
        # turn on/off LED when the button is pressed
        if myButton.value() == 0:
            myLED.toggle()
            # must have some sleep time to debounce the button
            utime.sleep(0.2)
            
except KeyboardInterrupt:
    myLED.off()