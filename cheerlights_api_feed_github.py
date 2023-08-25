# Place SSID and Password for Local Wifi here
SSID = 'your_SSID'
password = 'your_password'






# Code to interface with Cheerlights API
# HW for McWhorter's Pico W Course - Lesson 30
# Lori Pfahler
# August 2023

import network
import utime
import urequests

# function to connect to wifi
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
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
connect()

# request the current cheerlights feed data
cheerlights = urequests.get("http://api.thingspeak.com/channels/1417/feed.json").json()

# how many color changes in the feed
print('Number of color changes in the feed =', len(cheerlights['feeds']))

# to get a specific color request -
# position zero is the oldest in the feed.
print('Oldest Color Change:')
print(cheerlights['feeds'][0])

# get the current color - last in the feed data
print('Current Color Change:')
print(cheerlights['feeds'][len(cheerlights['feeds'])-1])

# get previous color
print('Next Previous Color Change:')
print(cheerlights['feeds'][len(cheerlights['feeds'])-2])

# get the next previous color
print('Next Next Previous Color Change:')
print(cheerlights['feeds'][len(cheerlights['feeds'])-3])


# get just the current color in hex and convert to RGB format
print('Current Color in HEX and RGB formats:')
print(cheerlights['feeds'][len(cheerlights['feeds'])-1]['field2'],
      hex_to_rgb(cheerlights['feeds'][len(cheerlights['feeds'])-1]['field2']))
# get current color as text
print('Current Color as Text:')
print(cheerlights['feeds'][len(cheerlights['feeds'])-1]['field1'])












