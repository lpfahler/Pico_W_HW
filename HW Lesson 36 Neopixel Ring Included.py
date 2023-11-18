# Homework for Pico W Course Lesson 36 - Neopixel Ring Included
# Control a Servo with a Potentiometer in MicroPython
# Lori Pfahler
# November 2023

# import modules
from machine import Pin, PWM, ADC
from utime import sleep
# download neopixel.py on pico w
from neopixel import Neopixel

# setup servo on GPIO 14 with frequency = 50Hz
myServo = PWM(Pin(14))
myServo.freq(50)
# min and max duty cycle
# each servo may need slightly different min and max to point to zero and 180 degreees
minDC = 0.5/20
maxDC = 2.5/20

# setup potentiometer on ADC0 GPIO26
myPot = machine.ADC(26)
# min and max potentiometer reading possible
# each potentiometer might give slightly different min and max
minPot = 500
maxPot = 65535

# setup neopixel ring
numPixels = 24
ring = Neopixel(numPixels, 0, 15, "GRBW")
ring.brightness(25)

try:
    while True:
        # read potentiometer
        potValue = myPot.read_u16()
        # calculate Duty Cycle for potValue
        # equation based on two points: (minPot, minDC), (maxPot, maxDC)
        DC = ((maxDC - minDC)/(maxPot - minPot))*(potValue - minPot) + minDC
        # send DC to servo scaled to 16-bit number needed for duty_u16()
        myServo.duty_u16(int(DC*65535))
        # calculate which neopixel to light
        pixelNum = int((-12/(maxDC - minDC))*(DC - minDC) + 12)
        ring.fill(rgb_w = (0, 0, 0))
        ring.set_pixel(pixelNum, rgb_w = (255, 255, 0))
        ring.show()
        sleep(0.05)      

except KeyboardInterrupt:
    # end with servo pointing at zero degrees
    myServo.duty_u16(int(minDC*65535))
    # clear neopixel ring
    ring.fill(rgb_w = (0, 0, 0))
    ring.show()



