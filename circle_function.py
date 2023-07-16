# Drawing a circle without the framebuf .ellispe() method
# Homework for McWhorter Pico W Lesson 25
# Lori Pfahler
# July 2023

# import modules
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep
import math

# setup I2C bus and display for "black" baord (yellow and blue on black)
i2c_1=I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
OLED1 = SSD1306_I2C(128, 64, i2c_1, addr = 0x3c)
OLED1.init_display()

# setup I2C bus and display for "blue" board (white on black)
i2c_2=I2C(0, sda = Pin(12), scl = Pin(13), freq = 400000)
OLED2 = SSD1306_I2C(128, 64, i2c_2, addr = 0x3c)
OLED2.init_display()

# function to create data to draw a circle
def circle(xcenter, ycenter, radius):
    # intialize list of xy pairs
    circle_values = []
    # create a list of angles in degrees for the circle
    angles = range(0, 360, 1)
    for deg in angles:
        # determine x and y pairs if center was at the origin
        # using conversion from polar coordinates to cartesian
        # convert angles in degrees to radians before taking sin() and cos()
        xorigin = radius*math.cos(deg*math.pi/180)
        yorigin = radius*math.sin(deg*math.pi/180)
        # adjust the x and y coordinates to actual center of the circle
        xshift = xorigin + xcenter
        yshift = yorigin + ycenter
        circle_values.append((int(xshift), int(yshift)))
    return(circle_values)

myPairs = circle(64, 32, 20)
for i in range(0, len(myPairs)):
    OLED1.pixel(myPairs[i][0], myPairs[i][1], 1)
OLED1.show()

for i in range(0, len(myPairs)):
    OLED2.pixel(myPairs[i][0], myPairs[i][1], 1)
OLED2.show()

sleep(10)

# clear the screen
OLED1.fill(0)
OLED1.show()
OLED2.fill(0)
OLED2.show()
        
    