# Program to read a potentiometer with averaging to
# improve precision of reading
# HW for Pico Lesson 5
# Lori Pfahler
# April 2023


# import modules
import machine
from utime import sleep

# setup potentiometers on ADC pins: ADC0 and ADC1
myPot = machine.ADC(28)

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
        sleep(0.1)
    potAvg = potSum/n
    return(potAvg)


while True:
    # read potentiometers
    potValue = read_pot(10, myPot)
    # read voltage scale y1 = 0, y2 = 3.3
    voltage = scale(potValue, 400, 65535, 0, 3.3)
    # eliminate negative voltages
    if voltage < 0:
        voltage = 0
    # HW challenge scale y1 = 100, y2 = 0 - negative slope
    hwValue = int(scale(potValue, 400, 65535, 100, 0))
    # print values to shell
    print('Voltage Scale hi:', potValue, '=', round(voltage, 3)) 
    print('Homework Scale:', potValue, '=', hwValue, '\n')
    sleep(2)
    

