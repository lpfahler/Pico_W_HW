# Homework from McWhorter's Lessons 45-46 on IMU6050
# Create the Tilt Meter - measure tilt in x and y directions
# Lori Pfahler
# January 2024

# import modules
from imu import MPU6050
from machine import I2C, Pin
from utime import sleep
from math import atan, pi
from ssd1306 import SSD1306_I2C

# setup I2C bus and mpu
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

# setup I2C bus and OLED display
i2c2=I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
myOLED = SSD1306_I2C(128, 64, i2c2, addr = 0x3c)
myOLED.init_display()

while True:
    # read acceleration in all directions from IMU
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    # x_tilt or Roll
    x_tilt_radians = atan(xAccel/zAccel)
    x_tilt_degrees = (x_tilt_radians * 180) / pi
    # y_tilt or Pitch
    y_tilt_radians = atan(yAccel/zAccel)
    y_tilt_degrees = (y_tilt_radians * 180) / pi
    # f-string for x and y tilt in yellow area of OLED
    # f-strings allow for exact control of decimal and rounding!
    myText = f'X: {x_tilt_degrees:3.0f}  Y: {y_tilt_degrees:3.0f}'
    myOLED.fill(0)
    myOLED.text(myText, 0, 0)
    # rectangle
    myOLED.rect(0, 16, 128, 48, 1)
    # horizontal and vertical lines
    myOLED.hline(0, 39, 128, 1)
    myOLED.vline(64, 16, 48, 1)
    # start of circle/bubble calculations - make it move with changes in x and y tilt
    ycenter = int(64 - y_tilt_degrees)
    # divided x by 2 to since there is less "room" for the x tilt direction
    xcenter = int(39 - x_tilt_degrees/2)
    # keep bubble out of yellow area on OLED
    if xcenter <= 21:
        xcenter = 21
    # x and y on display is opposite of x and y for IMU
    # due to the way I have oriented the IMU and display
    # place circle on OLED
    myOLED.ellipse(ycenter, xcenter, 5, 5, 1)
    myOLED.show()
    sleep(0.05)
    
    