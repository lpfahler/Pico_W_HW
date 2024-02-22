# Lesson 57 McWhorter's Pico W Course
# Working with the Joystick got me thinking ...
# Using a Rotary Encoder to move lighted pixel on Neopixel ring
# Lori Pfahler
# February 2024


# import modules
from utime import sleep_ms
# download rotary,py and rotary_irq_rp2.py to pico w
from rotary_irq_rp2 import RotaryIRQ
# download neopixel.py to pico w 
from neopixel import Neopixel

# setup Neopixel ring
ring = Neopixel(24, 1, 18, "GRBW")
ring.brightness(25)
ring.fill(rgb_w = (0, 0, 0))
ring.show()

# setup rotary encoder
rEncoder = RotaryIRQ(pin_num_clk=16, 
              pin_num_dt=17, 
              min_val=0, 
              max_val=23,
              # when using half_step=True - need to use reverse = True
              # not clear why that is needed
              reverse=False,
              # need to use half_step=True to get a change for each indent in my KY-040
              half_step = True,
              range_mode=RotaryIRQ.RANGE_WRAP)

# light first pixel on ring
valOld = rEncoder.value()
ring.set_pixel(valOld, rgb_w = (255, 0, 255))
ring.show()

try:
    while True:
        # read the encoder
        valNew = rEncoder.value()
        # move lighted pixel if there is a change in the encoder value
        if valOld != valNew:
            valOld = valNew
            ring.fill(rgb_w = (0, 0, 0))
            ring.set_pixel(valNew, rgb_w = (255, 0, 255))
            ring.show()
        sleep_ms(50)
    
except KeyboardInterrupt:
    ring.fill(rgb_w = (0, 0, 0))
    ring.show()