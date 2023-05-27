# Program to control RGB LED with three buttons plus a mystery button
# HW for McWhorter's Pico W Course Lesson 18
# Lori Pfahler
# May 2023

# import modules
from machine import Pin, PWM
from utime import sleep, ticks_ms, ticks_diff

# setup button and LED pins
redButton = Pin(18, Pin.IN, Pin.PULL_UP)
greenButton = Pin(17, Pin.IN, Pin.PULL_UP)
blueButton = Pin(16, Pin.IN, Pin.PULL_UP)
mysteryButton = Pin(22, Pin.IN, Pin.PULL_UP)

# setup red, green and blue for RGB LED
redLED_PWM = PWM(Pin(21))
redLED_PWM.freq(1000 )
redLED_PWM.duty_u16(0)
greenLED_PWM = PWM(Pin(20))
greenLED_PWM.freq(1000)
greenLED_PWM.duty_u16(0)
blueLED_PWM = PWM(Pin(19))
blueLED_PWM.freq(1000)
blueLED_PWM.duty_u16(0)

# variables to track interrupt activation, time for debouncing, led state
red_flag = 0
red_debounce_time = 0
red_state = False
green_flag = 0
green_debounce_time = 0
green_state = False
blue_flag = 0
blue_debounce_time = 0
blue_state = False
mystery_flag = 0
mystery_debounce_time = 0
delay_time = 0.3


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

# mystery interrupt function
def mystery_handler(mysteryButton):
    global mystery_flag, mystery_debounce_time
    if ticks_diff(ticks_ms(), mystery_debounce_time) > 300:
        mystery_flag = 1
        mystery_debounce_time = ticks_ms()

# interrupt request
redButton.irq(trigger = Pin.IRQ_RISING, handler = red_handler)
greenButton.irq(trigger = Pin.IRQ_RISING, handler = green_handler)
blueButton.irq(trigger = Pin.IRQ_RISING, handler = blue_handler)
mysteryButton.irq(trigger = Pin.IRQ_RISING, handler = mystery_handler)

# create a dictionary to hold the RGB codes for the colors
colors = {
    'violet'  : (148,   0, 211),
    'indigo'  : ( 75,   0, 130),
    'blue'    : (  0,   0, 255),
    'green'   : (  0, 255,   0),
    'yellow'  : (255, 150,   0),
    'orange'  : (255,  20,   0),
    'red'     : (255,   0,   0),
    'black'   : (  0,   0,   0)
    }


try:
    while True:
        # turn on/off red LED when the red button is pressed
        if red_flag == 1:
            red_flag = 0
            print("red button pressed")
            if red_state:
                # led is on - turn it off
                red_state = False
                redLED_PWM.duty_u16(colors.get('black')[0]<<8)
            else:
                # led is off - turn it on
                red_state = True
                redLED_PWM.duty_u16(colors.get('red')[0]<<8)

        # turn on/off green LED when the green button is pressed
        if green_flag == 1:
            green_flag = 0
            print("green button pressed")
            if green_state:
                # led is on - turn it off
                green_state = False
                greenLED_PWM.duty_u16(colors.get('black')[1]<<8)
            else:
                # led is off - turn it on
                green_state = True
                greenLED_PWM.duty_u16(colors.get('green')[1]<<8)
                
        # turn on/off blue LED when the blue button is pressed
        if blue_flag == 1:
            blue_flag = 0
            print("blue button pressed")
            if blue_state:
                # led is on - turn it off
                blue_state = False
                blueLED_PWM.duty_u16(colors.get('black')[2]<<8)
            else:
                # led is off - turn it on
                blue_state = True
                blueLED_PWM.duty_u16(colors.get('blue')[2]<<8)
                
        # mystery button is pressed        
        if mystery_flag == 1:
            mystery_flag = 0
            print('mystery button pressed!')
            # start the rainbow
            rainbow = ['violet', 'indigo', 'blue', 'green', 'yellow',
                       'orange', 'red', 'black']
            for color in rainbow:
                redLED_PWM.duty_u16(colors.get(color)[0]<<8)
                greenLED_PWM.duty_u16(colors.get(color)[1]<<8)
                blueLED_PWM.duty_u16(colors.get(color)[2]<<8)
                sleep(delay_time)
            print('mystery button finished')
             
except KeyboardInterrupt:
    redLED_PWM.duty_u16(colors.get('black')[0]<<8)
    greenLED_PWM.duty_u16(colors.get('black')[1]<<8)
    blueLED_PWM.duty_u16(colors.get('black')[2]<<8)

