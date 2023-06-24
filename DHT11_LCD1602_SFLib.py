# Program for DHT-11 Temp and Humidity Sensor
# Display on LCD1602
# Using a button to switch between degC to degF
# using "Blink Without Delay" Concept from Keith Lohmeyer
# to get a faster button response
# Lori Pfahler
# June 2023

# import needed modules
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin
from dht import DHT11
from lcd1602 import LCD

# setup DHT-11:  use internal pull-down resistor and setup as an output
# this is backwards to what you might think (should be an input)
DHT_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
myDHT11 = DHT11(DHT_pin)

# setup button
scaleButton = Pin(14, Pin.IN, Pin.PULL_UP)

# setup LCD - Using Sunfounder Library for LDC1602
myLCD = LCD()

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

# allow DHT11 to initialize
sleep(2)

# track time between reads of DHT-11 - intialize previous time
previous_time = ticks_ms()

# get initial reading and send to the LCD
myDHT11.measure()
humid = myDHT11.humidity()
tempC = myDHT11.temperature()
text_H = f'Humidity = {humid}%'
myLCD.write(0, 1, text_H)
text_C = f'Temp(C) = {tempC:5.1f}'
myLCD.write(0, 0, text_C)  

try:
    while True:
        # only read the DHT11 every two seconds but let the loop proceed
        if ticks_diff(ticks_ms(), previous_time) > 2000:
            myDHT11.measure()
            previous_time = ticks_ms()
            humid = myDHT11.humidity()
            tempC = myDHT11.temperature()
            # humidity only needs to update when we get a new reading
            text_H = f'Humidity = {humid}%'
            myLCD.write(0, 1, text_H)

        if scale_toggle == True:
            text_C = f'Temp(C) = {tempC:5.1f}'
            myLCD.write(0, 0, text_C)        
        else:
            tempF = (tempC * 1.8) + 32
            text_F = f'Temp(F) = {tempF:5.1f}'
            myLCD.write(0, 0, text_F)        

except KeyboardInterrupt:
    # myLCD.clear() did not work reliably for me - tried adding sleep as well
    # myLCD.clear()
    # code below works sometimes ...
    myLCD.write(0, 0, '                ')
    myLCD.write(0, 1, '                ')
    print('Done')