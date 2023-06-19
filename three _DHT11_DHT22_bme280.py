# Program for DHT-11, DHt-22 and BME280 Temp and Humidity Sensors
# Using a yellow pushbutton to switch between degC to degF
# and a red pushbutton to switch between sensors
# 
# Incorporates "Blink Without Delay" Concept - a tip from Keith Loymeyer
# to get faster button response
#
# Lori Pfahler
# June 2023

# import needed modules
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin, I2C
from dht import DHT11, DHT22
import bme280

#initialize I2C for BME280 sensor on address 0x76 (addr pin is connected to ground)
i2c=I2C(0,sda=Pin(4), scl=Pin(5), freq=400000)

# setup DHT-11 and DHT-22
DHT11_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
DHT22_pin = Pin(16, Pin.OUT, Pin.PULL_DOWN)
myDHT11 = DHT11(DHT11_pin)
myDHT22 = DHT22(DHT22_pin)

# setup pushbuttons: scale = yellow button, sensor = red button
scaleButton = Pin(14, Pin.IN, Pin.PULL_UP)
sensorButton = Pin(15, Pin.IN, Pin.PULL_UP)

# variable to track scale to use: True = degC; False = degF
scale_toggle = True
# variable for debouncing scale button in interrupt function
scale_debounce_time = ticks_ms()
# variable to track sensor to use: 1 = DHT11; 2 = DHT22; 3 = BME280
# using integers since final program will include two more sensors
switchSensor = 1
# variable for debouncing sensor button in interrupt function
sensor_debounce_time = ticks_ms()


# scaleButton interrupt function
def scale_handler(scaleButton):
    global scale_toggle, scale_debounce_time
    if ticks_diff(ticks_ms(), scale_debounce_time) > 300:
        scale_toggle = not scale_toggle
        scale_debounce_time = ticks_ms()

# sensorButton interrupt function
def sensor_handler(sensorButton):
    global switchSensor, sensor_debounce_time
    if ticks_diff(ticks_ms(), sensor_debounce_time) > 300:
        if switchSensor == 1:
            switchSensor = 2
        elif switchSensor == 2:
            switchSensor = 3
        else:
            switchSensor = 1
        sensor_debounce_time = ticks_ms()
        
# interrupt request
scaleButton.irq(trigger = Pin.IRQ_RISING, handler = scale_handler)
sensorButton.irq(trigger = Pin.IRQ_RISING, handler = sensor_handler)


# allow DHT11 and DHT22 to initialize
sleep(2)

# use "blink with delay" concept from Keith Loymeyer; initialize previous_time
previous_time = ticks_ms()

# function to get readings
def read_data():
    enviro_data = []
    myDHT11.measure()
    myDHT22.measure()
    # DHT11 results in index 0-2
    enviro_data.append(myDHT11.temperature())
    enviro_data.append((myDHT11.temperature() * 1.8) + 32)
    enviro_data.append(myDHT11.humidity())
    # DHT22 results in index 3-5
    enviro_data.append(myDHT22.temperature())
    enviro_data.append((myDHT22.temperature() * 1.8) + 32)
    enviro_data.append(myDHT22.humidity())
    # BME280 results in index 6-8 - data is reported as strings
    # example: ('21.22C', '970.15hPa', '60.36%')
    myBME280 = bme280.BME280(i2c=i2c, address = 0x76)
    # remove "C" from temp result and make a float 
    tempC = float(myBME280.values[0][:-1])
    tempF = (tempC * 1.8) + 32
    # remove "%" from humity result and make a float
    humidity = float(myBME280.values[2][:-1])
    enviro_data.append(tempC)
    enviro_data.append(tempF)
    enviro_data.append(humidity)

    return(enviro_data)

current_data = read_data()

try:   
    while True:
        # only read the sensors every two seconds but let the loop proceed
        if ticks_diff(ticks_ms(), previous_time) > 2000:
            current_data = read_data()
            previous_time = ticks_ms()
            
        if switchSensor == 1:
            if scale_toggle == True:
                print(f'DHT11: Temp = {current_data[0]:5.1f}{chr(176)}C, Humidity = {current_data[2]}% ', end = '\r')
            else:
                print(f'DHT11: Temp = {current_data[1]:5.1f}{chr(176)}F, Humidity = {current_data[2]}% ', end = '\r')

        if switchSensor == 2:
            if scale_toggle == True:
                print(f'DHT22: Temp = {current_data[3]:5.1f}{chr(176)}C, Humidity = {current_data[5]:2.0f}% ', end = '\r')
            else:
                print(f'DHT22: Temp = {current_data[4]:5.1f}{chr(176)}F, Humidity = {current_data[5]:2.0f}% ', end = '\r')

        if switchSensor == 3:
            if scale_toggle == True:
                print(f'BME280: Temp = {current_data[6]:5.1f}{chr(176)}C, Humidity = {current_data[8]:2.0f}%', end = '\r')
            else:
                print(f'BME280: Temp = {current_data[7]:5.1f}{chr(176)}F, Humidity = {current_data[8]:2.0f}%', end = '\r')


except KeyboardInterrupt:
    message = 'Done'
    print(f'{message:<50s}')