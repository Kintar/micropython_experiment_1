import time

from neopixel import Neopixel
from typing import Tuple
from machine import Pin

# set up some default colors
CLR_BLACK: Tuple[int, int, int] = (0, 0, 0)
CLR_ORANGE: Tuple[int, int, int] = (255, 50, 0)
CLR_BLUE: Tuple[int, int, int] = (0, 0, 255)

# numbers of pixels for our LEDs
NUM_SOLID_PIX = 7
NUM_SOLID_PIX_2 = 19
NUM_CHASE_PIX = 87

# pins we're connected to
PIN_SOLID_1 = 14
PIN_SOLID_2 = 15
PIN_CHASE = 16
PIN_TOGGLE = 17

# the LED areas
led_solid_1 = Neopixel(NUM_SOLID_PIX, 0, PIN_SOLID_1, "GRB", 0)
led_solid_2 = Neopixel(NUM_SOLID_PIX_2, 1, PIN_SOLID_2, "GRB", 0)
led_chase = Neopixel(NUM_CHASE_PIX, 2, PIN_CHASE, "GRB", 0)

toggle_pin = Pin(PIN_TOGGLE, mode=Pin.IN, pull=Pin.PULL_UP)

last_pin_state = 0
current_pin_state = 0

def show_leds() -> None:
    led_solid_1.show()
    led_solid_2.show()
    led_chase.show()

def switch_color(clr: Tuple[int, int, int]) -> None:
    led_solid_1.fill(CLR_BLACK)
    led_solid_2.fill(CLR_BLACK)
    led_chase.fill(CLR_BLACK)
    show_leds()

    led_solid_1.fill(clr)
    led_solid_2.fill(clr)
    led_chase.set_pixel_line_gradient(0, NUM_CHASE_PIX, clr, CLR_BLACK)
    show_leds()

def toggle_callback(pin):
    global current_pin_state
    current_pin_state = pin.value


toggle_pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=toggle_callback)

while True:
    led_chase.rotate_right(5)
    led_chase.show()
    if last_pin_state != current_pin_state:
        if current_pin_state == 0:
            switch_color(CLR_BLUE)
        else:
            switch_color(CLR_ORANGE)
        last_pin_state = current_pin_state
    time.sleep_us(200)

