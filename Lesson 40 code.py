# Code/HW from McWhorter's Lesson 40 on IMU6050
# Also used this code to demostrate measuring 0G
# in all directions (x, y, z) which occurs in freefall (HW Lesson 43)
# Lori Pfahler
# December 2023

# import modules
from imu import MPU6050
from machine import I2C, Pin
from utime import sleep

# setup I2C bus and mpu
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

# get acceleration data in x and y directions
# print code is commented out for including z direction
# use plotter to visualize when moving IMU 
while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    # when at rest zAccel should read 1G
    zAccel = mpu.accel.z
    # print(f'x: {xAccel:.4f} G, y: {yAccel:.4f} G')
    print(f'x: {xAccel:.4f} G, y: {yAccel:.4f} G, z: {zAccel:.4f} G')
    sleep(0.1)