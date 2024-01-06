# Homework from McWhorter's Lessons 41-43 on IMU6050
# Infer Tilt in x and y directions
# Lori Pfahler
# December 2023

# import modules
from imu import MPU6050
from machine import I2C, Pin
from utime import sleep
from math import atan, pi

# setup I2C bus and mpu
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

# get acceleration data in x and y directions
# use plotter to visualize when moving IMU 
while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    if xAccel > 1:
        xAccel = 1
    if yAccel > 1:
        yAccel = 1
    if zAccel > 1:
        zAccel = 1
    # the x_tilt is also called roll
    x_tilt_radians = atan(xAccel/zAccel)
    x_tilt_degrees = (x_tilt_radians * 180) / pi
    # the y_tilt is also called pitch
    y_tilt_radians = atan(yAccel/zAccel)
    y_tilt_degrees = (y_tilt_radians * 180) / pi
    print(f'x roll: {x_tilt_degrees:.0f} degrees | y pitch: {y_tilt_degrees:.0f} degrees')
    sleep(0.1)
