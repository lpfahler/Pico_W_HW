# Program for DHT-11 Temp and Humidity Sensor
# Using a button to switch between degC to degF
# Lori Pfahler
# June 2023

# import needed modules
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin
from dht import DHT11

# setup DHT-11:  use internal pull-down resistor and setup as an output
# this is backwards to what you might think (should be an input)
DHT_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
myDHT11 = DHT11(DHT_pin)

# setup button
scaleButton = Pin(16, Pin.IN, Pin.PULL_UP)

# variable to track scale to use: True = degC; False = degF
scale_toggle = True
# variable for debouncing button in interrupt function
scale_debounce_time = 0

# scaleButton interrupt function
def scale_handler(scaleButton):
    global scale_toggle, scale_debounce_time
    if ticks_diff(ticks_ms(), scale_debounce_time) > 300:
        scale_toggle = not scale_toggle
        scale_debounce_time = ticks_ms()
        
# interrupt request
scaleButton.irq(trigger = Pin.IRQ_RISING, handler = scale_handler)


while True:
    # use try and except to get reading from DHT-11 - otherwise may get
    # timeout error: OSError: [Errno 110] ETIMEDOUT
    try:
        myDHT11.measure()
    except:
        sleep(1)
    tempC = myDHT11.temperature()
    humid = myDHT11.humidity()
    if scale_toggle == True:
        print(f'Temp = {tempC:5.1f}{chr(176)}C, Humidity = {humid}%', end = '\r')
    else:
        tempF = (tempC * 1.8) + 32
        print(f'Temp = {tempF:5.1f}{chr(176)}F, Humidity = {humid}%', end = '\r')
    sleep(1)
