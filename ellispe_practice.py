# import modules
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from utime import sleep

# setup I2C bus and display for "black" baord (yellow and blue on black)
i2c_1=I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
OLED1 = SSD1306_I2C(128, 64, i2c_1, addr = 0x3c)
OLED1.init_display()

# more with ellipse()
OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b0001) # upper right
OLED1.show()

sleep(1)

OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b0010) # upper left
OLED1.show()

sleep(1)

OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b0100) # lower left
OLED1.show()

sleep(1)

OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b1000) # lower right
OLED1.show()

sleep(1)

OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b0011) # upper right and left
OLED1.show()

sleep(1)

OLED1.fill(0)
OLED1.ellipse(64, 32, 30, 15, 1, True, 0b0101) # upper right and lower left
OLED1.show()

sleep(3)

# clear the screen
OLED1.fill(0)
OLED1.show()

