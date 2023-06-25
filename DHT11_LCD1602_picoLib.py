# Program for DHT-11 Temp and Humidity Sensor
# Display on LCD1602 using pico_i2c_lcd library
# Using a button to switch between degC to degF
# using "Blink Without Delay" Concept from Keith Lohmeyer
# to get a faster button response
# Lori Pfahler
# June 2023

# import needed modules
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin, I2C
from dht import DHT11
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# setup LCD - Using pico_i2c_lcd Library for LDC1602
I2C_ADDR     = 0x3f
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7), freq=400000)
myLCD = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS) 

# setup DHT-11:  use internal pull-down resistor and setup as an output
# this is backwards to what you might think (should be an input)
DHT_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
myDHT11 = DHT11(DHT_pin)

# setup button
scaleButton = Pin(14, Pin.IN, Pin.PULL_UP)

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

# a function to create a custom character 
def customcharacter():    
    #degree symbol      
    myLCD.custom_char(0, bytearray([
    0x0E,
    0x0A,
    0x0E,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00]))

# run the function
customcharacter()

# track time between reads of DHT-11 - intialize previous time
previous_time = ticks_ms()

# get initial reading and send to the LCD
myDHT11.measure()
humid = myDHT11.humidity()
tempC = myDHT11.temperature()
text_H = f'Humidity = {humid}%'
myLCD.move_to(0,1)
myLCD.putstr(text_H)
# {chr(0)} suggested by Keith Lohmeyer to simplify the code - works
text_C = f'Temp = {tempC:4.1f}{chr(0)}C'
myLCD.move_to(0,0)
myLCD.putstr(text_C)
# old code:
# myLCD.move_to(11,0)
# add in custom character - degree symbol
# myLCD.putchar(chr(0))
# myLCD.move_to(12,0) 
# myLCD.putstr('C')

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
            myLCD.move_to(0,1)
            myLCD.putstr(text_H)

        if scale_toggle == True:
            text_C = f'Temp = {tempC:4.1f}{chr(0)}C '
            myLCD.move_to(0,0)
            myLCD.putstr(text_C)
        else:
            tempF = (tempC * 1.8) + 32
            text_F = f'Temp = {tempF:5.1f}{chr(0)}F'
            myLCD.move_to(0,0)
            myLCD.putstr(text_F)

except KeyboardInterrupt:
    myLCD.clear()