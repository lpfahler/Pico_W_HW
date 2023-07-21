# A program to draw some Lissajous Curves on a SSD1306 display
# Lori Pfahler
# July 2023

# import modules
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep
import math

# setup I2C bus and display for "blue" board (white on black)
i2c = I2C(0, sda = Pin(12), scl = Pin(13), freq = 300000)
OLED = SSD1306_I2C(128, 64, i2c, addr = 0x3c)
OLED.init_display()

# x = A*sin(a*t + delta)
# y = B*sin(b*t)
# variables:
# magnitude of curves in x direction
A = 40

# magniture of curves in y direction
B = 20

# the a to b ratio must be in whole numbers
# to get closed curve e.g. a/b = 1/2, 1/3, 2/3
# if you  a > b (a/b = 2/1), you can switch the orientation
# a/b = 1/2 gives a good rotating potato chip
a = 2
b = 3

# cycle t through 0 to 2pi to get one curve
# cycle delta through 0 to 2pi to create motion 

try:
    while True:
        for delta in range(0, 360, 5):
            for t in range(0, 360, 1):
                # add 64 and 32 to center the curves
                x = A*math.sin(a*math.radians(t) + math.radians(delta)) + 64
                y = B*math.sin(b*math.radians(t)) + 32
                # print(int(x), int(y))      
                OLED.pixel(int(x), int(y), 1)
            OLED.show()
            # clear the screen
            OLED.fill(0)

except KeyboardInterrupt:
    # clear the screen
    OLED.fill(0)
    OLED.show()  
