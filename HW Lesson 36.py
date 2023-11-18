# Homework for Pico W Course Lesson 36
# Control a Servo with a Potentiometer in MicroPython
# Lori Pfahler
# November 2023

# import modules
from machine import Pin, PWM, ADC
from utime import sleep

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


try:
    while True:
        # read potentiometer
        potValue = myPot.read_u16()
        # calculate Duty Cycle for potValue
        # equation based on two points: (minPot, minDC), (maxPot, maxDC)
        DC = ((maxDC - minDC)/(maxPot - minPot))*(potValue - minPot) + minDC
        # send DC to servo scaled to 16-bit number needed for duty_u16()
        myServo.duty_u16(int(DC*65535))
        sleep(0.01)      

except KeyboardInterrupt:
    # end with servo pointing at zero degrees
    myServo.duty_u16(int(minDC*65535))
