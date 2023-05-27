# Program to control RGB LED with three buttons
# HW for McWhorter's Pico W Course Lesson 18
# Lori Pfahler
# May 2023

# import modules
from machine import Pin, PWM
from utime import ticks_ms, ticks_diff

# setup button and LED pins
redButton = Pin(18, Pin.IN, Pin.PULL_UP)
greenButton = Pin(17, Pin.IN, Pin.PULL_UP)
blueButton = Pin(16, Pin.IN, Pin.PULL_UP)
redLED = Pin(21, Pin.OUT)
greenLED = Pin(20, Pin.OUT)
blueLED = Pin(19, Pin.OUT)

# variables to track interrupt activation, time for debouncing
red_flag = 0
red_debounce_time = 0
green_flag = 0
green_debounce_time = 0
blue_flag = 0
blue_debounce_time = 0

# red interrupt function
def red_handler(redButton):
    global red_flag, red_debounce_time
    if ticks_diff(ticks_ms(), red_debounce_time) > 300:
        red_flag = 1
        red_debounce_time = ticks_ms()

# green interrupt function
def green_handler(greenButton):
    global green_flag, green_debounce_time
    if ticks_diff(ticks_ms(), green_debounce_time) > 300:
        green_flag = 1
        green_debounce_time = ticks_ms()

# blue interrupt function
def blue_handler(blueButton):
    global blue_flag, blue_debounce_time
    if ticks_diff(ticks_ms(), blue_debounce_time) > 300:
        blue_flag = 1
        blue_debounce_time = ticks_ms()

# interrupt request
redButton.irq(trigger = Pin.IRQ_RISING, handler = red_handler)
greenButton.irq(trigger = Pin.IRQ_RISING, handler = green_handler)
blueButton.irq(trigger = Pin.IRQ_RISING, handler = blue_handler)

try:
    while True:
        # turn on/off red LED when the red button is pressed
        if red_flag == 1:
            red_flag = 0
            print("red button pressed")
            redLED.toggle()
            
        # turn on/off green LED when the green button is pressed
        if green_flag == 1:
            green_flag = 0
            print("green button pressed")
            greenLED.toggle()
                
        # turn on/off blue LED when the blue button is pressed
        if blue_flag == 1:
            blue_flag = 0
            print("blue button pressed")
            blueLED.toggle()            
                
except KeyboardInterrupt:
    redLED.off()
    greenLED.off()
    blueLED.off()

