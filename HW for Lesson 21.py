# Program for DHT-11 Temp and Humidity Sensor
# Using a button to switch between deg, degF and Humidity
# using "Blink Without Delay" Concept from Keith Loymeyer
# to get a faster button response
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
readingButton = Pin(14, Pin.IN, Pin.PULL_UP)

# variable to track what reading to output: 1 = Temp degC; 2 = Temp degF; 3 = Humidity
reading_toggle = 1
# variable for debouncing button in interrupt function
reading_debounce_time = 0

# readingButton interrupt function
def reading_handler(readingButton):
    global reading_toggle, reading_debounce_time
    if ticks_diff(ticks_ms(), reading_debounce_time) > 300:
        # could be done with module math but I think this code easier to read
        if reading_toggle == 1:
            reading_toggle = 2
        elif reading_toggle == 2:
            reading_toggle = 3
        else:
            reading_toggle = 1
        reading_debounce_time = ticks_ms()
        
# interrupt request
readingButton.irq(trigger = Pin.IRQ_RISING, handler = reading_handler)

# allow DHT11 to initialize
sleep(2)

# use "blink without delay" concept from Keith Loymeyer
previous_time = ticks_ms()

# get initial reading and assign/calculate readings
myDHT11.measure()
tempC = myDHT11.temperature()
tempF = (tempC * 1.8) + 32
humid = myDHT11.humidity()

try:
    while True:
        # only read the DHT11 every two seconds but let the loop proceed
        if ticks_diff(ticks_ms(), previous_time) > 2000:
            myDHT11.measure()
            # reset previous_time
            previous_time = ticks_ms()
            # assign/calculate readings
            tempC = myDHT11.temperature()
            tempF = (tempC * 1.8) + 32
            humid = myDHT11.humidity()
        # print appropriate reading
        if reading_toggle == 1:
            print(f'Temp = {tempC:5.1f}{chr(176)}C    ', end = '\r')
        elif reading_toggle == 2:            
            print(f'Temp = {tempF:5.1f}{chr(176)}F    ', end = '\r')
        else:
            print(f'Humidity = {humid}%', end = '\r')


except KeyboardInterrupt:
    message = 'Done'
    print(f'{message:<50s}')