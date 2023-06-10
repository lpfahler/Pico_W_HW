# Program for DHT-11 Temp and Humidity Sensor
# From Lesson 20 McWhorter's Pico W

from machine import Pin
from utime import sleep
from dht import DHT11

# use internal pull-down resistor and setup as an output
# this is backwards to what you might think (should be an input)
# has to do with the way the library is written I guess
DHT_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
myDHT11 = DHT11(DHT_pin)

while True:
    # use try and except to get reading from DHT-11 - otherwise may get
    # timeout error: OSError: [Errno 110] ETIMEDOUT
    try:
        myDHT11.measure()
    except:
        sleep(1)
    # myDHT11.measure()
    tempC = myDHT11.temperature()
    
    humid = myDHT11.humidity()
    print(f'Temp = {tempC}{chr(176)}C, Humidity = {humid}%', end = '\r')
    sleep(1)
    