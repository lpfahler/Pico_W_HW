# Program to turn an LED on and off with a Button
# Address holding button for longer than sleep time for debouncing
# Will go on or off only once no matter how long I hold the button
# Lori Pfahler
# May 2023

# import modules
from machine import Pin
import utime

# setup button and LED pins
myButton = Pin(12, Pin.IN, Pin.PULL_UP)
myLED = Pin(15, Pin.OUT)

# variable to keep track of the button value from the previous loop
buttonPrevious = 1

try:
    while True:
        # read the current state of the pushbutton
        buttonCurrent = myButton.value()
        # below is the state of the two variables that indicates the
        # button has been pressed AND let go of
        if (buttonPrevious==0 and buttonCurrent==1):
            myLED.toggle()
            utime.sleep(0.1)
        # reset buttonPrevious to buttonCurrent and loop again
        buttonPrevious = buttonCurrent
        
except KeyboardInterrupt:
    myLED.off()
