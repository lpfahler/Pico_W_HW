# Lesson 31 HW McWhorters Pico W Course
# Lori Pfahler
# September 2023


import urequests
import connect_wifi
import utime
from neopixel import Neopixel
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# setup Temperature Neopixel
oneNeo = Neopixel(1, 0, 10, "GRBW")
oneNeo.brightness(25)
oneNeo.fill(rgb_w = (0, 0, 0))
oneNeo.show()

# setup wind direction and speed Neopixel ring
ring = Neopixel(24, 1, 0, "GRBW")
ring.brightness(25)
ring.fill(rgb_w = (0, 0, 0))
ring.show()

# setup I2C bus and SSD1306 display (white on black)
myI2C = I2C(0, sda = Pin(12), scl = Pin(13), freq = 400000)
myOLED = SSD1306_I2C(128, 64, myI2C, addr = 0x3c)
myOLED.init_display()


# function to get the weather info from open weather map API
# returns a dictionary of results
def getWxr(loc='quakertown,pa,us'):
    # get weather information for requested location
    myURL = f'https://api.openweathermap.org/data/2.5/weather?q={loc}&appid=20622fba82834a841871f445f00d9e78&units=imperial'
    wxr = urequests.get(myURL).json()
    # get date and time info - add in timezone to my local time
    dt = utime.localtime(wxr['dt'] + wxr['timezone'])
    strDate = f'Date: {dt[1]}/{dt[2]}/{dt[0]}'
    strTime = f'Time: {dt[3]}:{dt[4]}'
    wxrDict = {'date': strDate, 'time': strTime}
    # location
    strCountry = wxr['sys']['country']
    strCity = wxr['name']
    wxrDict['country'] = strCountry
    wxrDict['city'] = strCity
    # sunrise and sunset
    sunrise = utime.localtime(wxr['sys']['sunrise'] + wxr['timezone'])
    strSunrise = f'Sunrise: {sunrise[3]}:{sunrise[4]}'
    wxrDict['sunrise'] = strSunrise
    sunset = utime.localtime(wxr['sys']['sunset'] + wxr['timezone'])
    strSunset = f'Sunset: {sunset[3]}:{sunset[4]}'
    wxrDict['sunset'] = strSunset
    # temp
    curTemp = wxr['main']['temp']
    strTemp = f'Temp: {curTemp:4.1f} F'
    wxrDict['temp'] = [curTemp, strTemp]
    # humidity
    curHumid = wxr['main']['humidity']
    strHumid = f'Humid: {curTemp:4.1f}%'
    wxrDict['humid'] = [curHumid, strHumid]
    # barometric pressure in atmospheres - should be close to 1
    # with conversion from hPa to ATM
    pressure = wxr['main']['pressure']*0.0009869233
    strPressure = f'Pr: {pressure:6.4f} ATM'
    wxrDict['pressure'] = [pressure, strPressure]
    # current conditions
    # might be more than one condition so need to index through the list
    # but I will only use the first one in this project
    curCond = wxr['weather'][0]['main']
    strCond = f'{curCond}'
    curDesc = wxr['weather'][0]['description']
    strDesc = f'{curDesc}'
    wxrDict['conditions'] = [strCond, strDesc]
    # wind speed and direction
    windSpeed = wxr['wind']['speed']
    windDir = wxr['wind']['deg']
    strWindSpeed = f'Speed: {windSpeed:4.1f} mph'
    strWindDir = f'Wind Dir: {windDir}'
    wxrDict['wspeed'] = [windSpeed, strWindSpeed]
    wxrDict['wdir'] = [windDir, strWindDir]
    return(wxrDict)


# connect to wifi
connect_wifi.connect()

# get first reading of weather
curWeather = getWxr()

# breadboard neopixel for temp reading
if curWeather['temp'][0] <= 32:
    oneNeo.set_pixel(0, rgb_w = (0, 0, 255))
elif curWeather['temp'][0] > 32 and curWeather['temp'][0] <= 50:
    oneNeo.set_pixel(0, rgb_w = (0, 255, 255))
elif curWeather['temp'][0] > 50 and curWeather['temp'][0] <= 80:
    oneNeo.set_pixel(0, rgb_w = (0, 255, 0))
else:
    oneNeo.set_pixel(0, rgb_w = (255, 0, 0))
oneNeo.show()

# indicate direction of wind and speed on neopixel ring
windPixel = (curWeather['wdir'][0]/15)
if curWeather['wspeed'][0] <= 5:
    ring.set_pixel(int(windPixel), rgb_w = (0, 255, 0))
elif curWeather['wspeed'][0] > 5 and curWeather['wspeed'][0] <= 15:
    ring.set_pixel(int(windPixel), rgb_w = (255, 255, 0))
else:
    ring.set_pixel(int(windPixel), rgb_w = (255, 0, 0))
ring.show()
    
# use "blink with delay" concept - initialize previous_time
previous_time = utime.ticks_ms()

while True:
    #  query API every 5 minutes but let the loop proceed
    if utime.ticks_diff(utime.ticks_ms(), previous_time) > 60000:
        myOLED.fill(0)
        myOLED.text('Conditions at', 0, 0)
        myOLED.text(curWeather['city'], 0, 9)
        myOLED.text('Getting', 0, 28)
        myOLED.text('new data', 0, 38)
        myOLED.show()
        curWeather = getWxr()
        previous_time = utime.ticks_ms()           
        # update neopixel for temp reading
        if curWeather['temp'][0] <= 32:
            oneNeo.set_pixel(0, rgb_w = (0, 0, 255))
        elif curWeather['temp'][0] > 32 and curWeather['temp'][0] <= 50:
            oneNeo.set_pixel(0, rgb_w = (0, 255, 255))
        elif curWeather['temp'][0] > 50 and curWeather['temp'][0] <= 80:
            oneNeo.set_pixel(0, rgb_w = (0, 255, 0))
        else:
            oneNeo.set_pixel(0, rgb_w = (255, 0, 0))
        oneNeo.show()
        # update direction of wind and speed on neopixel ring
        ring.fill(rgb_w = (0, 0, 0))
        windPixel = (curWeather['wdir'][0]/15)
        if curWeather['wspeed'][0] <= 5:
            ring.set_pixel(int(windPixel), rgb_w = (0, 255, 0))
        elif curWeather['wspeed'][0] > 5 and curWeather['wspeed'][0] <= 15:
            ring.set_pixel(int(windPixel), rgb_w = (255, 255, 0))
        else:
            ring.set_pixel(int(windPixel), rgb_w = (255, 0, 0))
        ring.show()
        utime.sleep(10)

    
    myOLED.fill(0)
    myOLED.text('Conditions at', 0, 0)
    myOLED.text(curWeather['city'], 0, 9)
    myOLED.text(curWeather['temp'][1], 0, 28)
    myOLED.text(curWeather['wdir'][1], 0, 38)
    myOLED.text(curWeather['wspeed'][1], 0, 48)
    myOLED.show()

    utime.sleep(10)
    
    myOLED.fill(0)
    myOLED.text(curWeather['date'], 0, 0)
    myOLED.text(curWeather['time'], 0, 9)
    myOLED.text(curWeather['humid'][1], 0, 28)
    myOLED.text(curWeather['pressure'][1], 0, 38)
    myOLED.text(curWeather['conditions'][0], 0, 48)
    myOLED.show()
    
    utime.sleep(10)
    
    myOLED.fill(0)
    myOLED.text('More Info', 0, 0)
    myOLED.text(curWeather['city'], 0, 9)
    myOLED.text(curWeather['sunrise'], 0, 28)
    myOLED.text(curWeather['sunset'], 0, 38)
    myOLED.show()
    
    utime.sleep(10)