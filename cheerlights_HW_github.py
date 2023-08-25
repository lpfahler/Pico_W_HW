# Place SSID and Password for Local Wifi here
SSID = 'your_SSID'
password = 'your_password'






# Code to interface with Cheerlights API
# Light RGB LED (current color) and Neopixel Ring with Past Colors
# HW for McWhorter's Pico W Course - Lesson 30
# Lori Pfahler
# August 2023

import network
import utime
import urequests
# use picozero library for control of RGB LED
# install from Tools Menu ... Manage packages in Thonny
from picozero import RGBLED
# must load neopixel.py on pico
from neopixel import Neopixel
from machine import Pin, I2C
# must load ssd1306.py on pico
from ssd1306 import SSD1306_I2C

# setup RGB LED object
rgb = RGBLED(red = 9, green = 8, blue = 7)

# setup neopixel ring
numpix = 16
strip = Neopixel(numpix, 0, 0, "GRBW")
strip.brightness(25)

# setup I2C bus and SSD1306 display (white on black)
myI2C = I2C(0, sda = Pin(12), scl = Pin(13), freq = 400000)
myOLED = SSD1306_I2C(128, 64, myI2C, addr = 0x3c)
myOLED.init_display()

# function to connect to wifi
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, password)
    while wlan.isconnected() == False:
        # comment this print out if running on pico independent of computer
        print('Waiting for connection...')
        utime.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return(ip)

# function to convert hex color format to RGB format
def hex_to_rgb(hexValue):
    hexColor= hexValue.lstrip('#')
    redValue = int(hexColor[0:2], 16)
    greenValue = int(hexColor[2:4], 16)
    blueValue = int(hexColor[4:6], 16)
    combinedValues = (redValue, greenValue, blueValue)
    return(combinedValues)


# connect to wifi
serverIP = connect()

# Show Server IP address on display
myOLED.rect(0, 0, 127, 9, 0, True)
myOLED.text(serverIP, 0, 0)
myOLED.hline(0, 10, 127, 1)
myOLED.show()


try:
    while True:
        myOLED.rect(0, 16, 127, 47, 0, True)
        # print this just so we can see that the program is actually running
        myOLED.text('Checking ...', 0, 16)
        myOLED.show()
        utime.sleep(5)
        # request the current cheerlights feed data
        cheerlights = urequests.get("http://api.thingspeak.com/channels/1417/feed.json").json()
        # get current cheerlights color and convert to rgb format
        currentColor = hex_to_rgb(cheerlights['feeds'][len(cheerlights['feeds'])-1]['field2'])
        # put current color on RGB LED
        rgb.color = currentColor
        
        # past 16 colors on neopixel ring
        for i in range(16):
            rgbValue = hex_to_rgb(cheerlights['feeds'][len(cheerlights['feeds'])-(1 + i)]['field2'])
            strip.set_pixel(i, rgb_w = rgbValue)
        strip.show()
        
        # print current color and rgb values to the OLED
        myOLED.rect(0, 16, 127, 47, 0, True)
        myOLED.text('Current Color:', 0, 16)
        myOLED.text(cheerlights['feeds'][len(cheerlights['feeds'])-1]['field1'].upper(), 8, 26)
        myOLED.text('Red = ' + str(currentColor[0]), 0, 36)
        myOLED.text('Green = ' + str(currentColor[1]), 0, 46)
        myOLED.text('Blue = ' + str(currentColor[2]), 0, 56)
        myOLED.show()
        
        # time before checking API for a color change
        # recommend 5 or 10 minutes if program is left running
        utime.sleep(60)

except KeyboardInterrupt:
    rgb.color = (0, 0, 0)
    strip.fill(rgb_w = (0, 0, 0))
    strip.show()
    myOLED.fill(0)
    myOLED.show()




