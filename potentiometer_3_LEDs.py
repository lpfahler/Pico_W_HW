# Program to read a potentiometer to control 3 LEDs
# with averaging to improve precision of reading
# HW for Pico Lesson 6-8
# Lori Pfahler
# April 2023


# import modules
import machine
from utime import sleep

# setup potentiometer
myPot = machine.ADC(28)

# setup red, yellow and green LEDs
redLED = machine.Pin(13, machine.Pin.OUT)
yellowLED = machine.Pin(14, machine.Pin.OUT)
greenLED = machine.Pin(15, machine.Pin.OUT)

# function to scale x to y based on range of x and y
def scale(value, x1, x2, y1, y2):
    slope = (y2 - y1)/(x2 - x1)
    scaled_value = slope * (value - x1) + y1
    return(scaled_value)

# function to get an average value for potentiometer
def read_pot(n, potName):
    potSum = 0
    for i in range(0, n):
        potSum = potName.read_u16() + potSum
        sleep(0.0001)
    potAvg = potSum/n
    return(potAvg)

try:
    while True:
        # read potentiometers
        potValue = read_pot(10, myPot)
        # create scale y1 = 0 to y2 = 100
        # went to y2 = 101 to make sure the upper limit was 100
        # averaging was reducing the chances of seeing a 100
        myReading = scale(potValue, 400, 65535, 0, 101)
        # make sure myReading is in 0-100
        if myReading > 100:
            myReading = 100
        if myReading < 0:
            myReading = 0
        # print values to shell 
        print('{:3}'.format(int(myReading)), end = '\r')
        # light the proper LED
        if myReading < 80:
            greenLED.on()
            yellowLED.off()
            redLED.off()
        elif myReading >= 80 and myReading < 95:
            greenLED.off()
            yellowLED.on()
            redLED.off()
        else:
            greenLED.off()
            yellowLED.off()
            redLED.on()        
        sleep(0.5)
        
except KeyboardInterrupt:
    greenLED.off()
    yellowLED.off()
    redLED.off()    
