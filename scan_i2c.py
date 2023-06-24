from machine import Pin, I2C

i2c=I2C(1,sda=Pin(6), scl=Pin(7), freq=400000)
# Print out any addresses found
devices = i2c.scan()
if devices:
    for d in devices:
        print(hex(d))