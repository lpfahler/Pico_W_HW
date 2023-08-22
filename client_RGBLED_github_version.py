# HW for Lesson 28 Connecting the Pico to WiFi
# Client code on my Mac to control an RGB LED
# Lori Pfahler
# August 2023

# import modules
import socket

# setup client 
# the server address must match assigned IP address assigned to pico server
serverAddress = ('Pico_Server_IP_here', 2023)
bufferSize = 1024
UDPClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# infinite loop asking for RGB format of color from user
print('Enter the red, green, blue values for the color in RGB format')
print('Values should be within 0-255; values > 255 will be set to 255')
print('Example:  255 255 0 for red = 255, green = 255 and blue = 0')
while True:
    cmd = input('What color do you wish? ')
    # check to see if user entered three nonzero integers
    # if a value larger than 255 is entered, server will set it = 255
    while [x.isdigit() for x in cmd.split()] != [True, True, True]:
        cmd = input('Invalid Entry - What color do you wish? ')
    cmdEncoded = cmd.encode('utf-8')
    UDPClient.sendto(cmdEncoded, serverAddress)

