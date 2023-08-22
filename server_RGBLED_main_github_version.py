# Place Your SSID and Password for your Local Wifi here
SSID = 'Your SSID'
password = 'Your Password'






# HW for Lesson 28 Connecting the Pico to WiFi
# Server code on the pico to control an RGB LED
# Lori Pfahler
# August 2023

# import modules
import socket
import utime
import network
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

# setup I2C bus and SSD1306 display (white on black)
myI2C = I2C(0, sda = Pin(12), scl = Pin(13), freq = 400000)
myOLED = SSD1306_I2C(128, 64, myI2C, addr = 0x3c)
myOLED.init_display()

# Setup RGB LED
redLED = PWM(Pin(9))
redLED.freq(1000)
redLED.duty_u16(0)
greenLED = PWM(Pin(8))
greenLED.freq(1000)
greenLED.duty_u16(0)
blueLED = PWM(Pin(7))
blueLED.freq(1000)
blueLED.duty_u16(0)

# setup server
myWiFi = network.WLAN(network.STA_IF)
myWiFi.active(True)

# connect to local Wifi
myWiFi.connect(SSID, password)

# wait for connection to be made
while myWiFi.isconnected() == False:
    myOLED.text('Getting Wifi', 0, 0)
    utime.sleep(1)

# get IP address
serverIP = myWiFi.ifconfig()[0]

# Show Server IP address on display
myOLED.rect(0, 0, 127, 9, 0, True)
myOLED.text(serverIP, 0, 0)
myOLED.hline(0, 10, 127, 1)
myOLED.show()

# set port and buffer size
# port is 16-bit number, 0 - 65535, typically use a value above 1024
serverPort = 2023
bufferSize = 1024

# create server
UDPServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServer.bind((serverIP, serverPort))
myOLED.text('Server Ready', 0, 16)
myOLED.hline(0, 26, 127, 1)
myOLED.show()

# infinite loop to receive messages from client
while True:
    message, address = UDPServer.recvfrom(bufferSize)
    messageDecoded = message.decode('utf-8')
    # list comprehension to get red, green and blue values as a list of integers
    rgbList = [int(x) for x in messageDecoded.split()]
    # check to see if value is greater than 255 - if True, set value to 255
    for i in range(3):
        if rgbList[i] > 255:
            rgbList[i] = 255
    # Send RGB color values to display
    myOLED.rect(0, 16, 127, 47, 0, True)
    myOLED.text('Color Received', 0, 16)
    myOLED.hline(0, 26, 127, 1)
    myOLED.text('Red = ' + str(rgbList[0]), 0, 30)
    myOLED.text('Green = ' + str(rgbList[1]), 0, 40)
    myOLED.text('Blue = ' + str(rgbList[2]), 0, 50)    
    myOLED.show()
    # send color to RGB LED
    redLED.duty_u16(rgbList[0]<<8)
    greenLED.duty_u16(rgbList[1]<<8)
    blueLED.duty_u16(rgbList[2]<<8)
    utime.sleep(2)
    myOLED.rect(0, 16, 127, 8, 0, True)
    myOLED.text('Server Ready', 0, 16)
    myOLED.show()








