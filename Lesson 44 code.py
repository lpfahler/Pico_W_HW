# Code/HW from McWhorter's Lesson 44 and 45 on IMU6050
# Measure drop distance using accelerometer on IMU
# Lori Pfahler
# January 2024

# import modules
from imu import MPU6050
from machine import I2C, Pin
from utime import sleep, ticks_ms, ticks_diff
from ssd1306 import SSD1306_I2C

# setup I2C bus and mpu
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

# setup I2C bus and OLED display
i2c=I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
myOLED = SSD1306_I2C(128, 64, i2c, addr = 0x3c)
myOLED.init_display()

# indicator variable for a drop
drop = False

# while true loop will continuely update startTime and stopTime
# until a drop occurs indicated by zAccel dropping below 0.95G
while True:
    zAccel = mpu.accel.z
    myOLED.fill(0)
    myOLED.text('Drop when ready', 0, 0)
    myOLED.show()
    startTime = ticks_ms()
    while zAccel < 0.95:
        # a drop has occurred stay in this loop till zAccel gets back to 1G
        zAccel = mpu.accel.z  
        drop = True
        sleep(0.001)
    stopTime = ticks_ms()      
    if drop == True:
        # calculate drop time and distance if drop has occurred
        dropTime = ticks_diff(stopTime, startTime)/1000
        distance_inches = 0.5 * (32 * 12) * (dropTime**2)
        distance_cm = 0.5 * 980.66 * (dropTime**2)
        # put results on OLED
        myOLED.fill(0)
        myOLED.text("Drop Distance:", 0, 0)
        # use f-string to create string to print to OLED
        inch_text = f'inches: {distance_inches:3.1f}'
        myOLED.text(inch_text, 0, 16)
        # use f-string to create string to print to OLED
        cm_text = f'cm: {distance_cm:3.1f}'
        myOLED.text(cm_text, 0, 32)
        myOLED.show()        
        # must sleep a second or so to not register bouncing around after the drop
        sleep(5)
        # reset drop variable to false
        drop = False
    sleep(0.001)    
