# A program to draw some text and some circles on SSD1306 displays
# Lori Pfahler
# July 2023


# import modules
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep

# setup I2C bus and display for "black" baord (yellow and blue on black)
i2c_1=I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
OLED1 = SSD1306_I2C(128, 64, i2c_1, addr = 0x3c)
OLED1.init_display()

# setup I2C bus and display for "blue" board (white on black)
i2c_2=I2C(0, sda = Pin(12), scl = Pin(13), freq = 400000)
OLED2 = SSD1306_I2C(128, 64, i2c_2, addr = 0x3c)
OLED2.init_display()

# display some text
OLED1.text("Welcome to", 0, 0)
OLED1.text("Lori's Robots", 0, 16)
OLED1.show()

OLED2.text("Welcome to", 0, 0)
OLED2.text("Lori's Robots", 0, 16)
OLED2.show()

sleep(5)

# easy solution to homework!

# circle outline
OLED1.fill(0)
OLED1.ellipse(64, 32, 20, 20, 1)
OLED1.show()

# circle filled
OLED2.fill(0)
OLED2.ellipse(64, 32, 20, 20, 1, True)
OLED2.show()

sleep(5)

# clear the screen
OLED1.fill(0)
OLED1.show()
OLED2.fill(0)
OLED2.show()



