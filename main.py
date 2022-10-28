# Trinket IO demo
# Welcome to CircuitPython :)

from touchio import *
from digitalio import *
from analogio import *
from board import *
import time
import neopixel
import random

# Capacitive touch on D1
touch = TouchIn(D1)

# NeoPixel strip (of 16 LEDs) connected on D3
NUMPIXELS = 27
neopixels = neopixel.NeoPixel(D3, NUMPIXELS, brightness=1, auto_write=True)
DIRECTION = 1 # 1 == "up"
COLOR = 1 # 1 == "red"
CHASECOLOR = 0

######################### HELPERS ##############################

# Helper to convert analog input to voltage
# def getVoltage(pin):
#     return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def flicker(idx, rgbVal):
    neopixels[idx] = rgbVal
    if idx > 2 and idx < NUMPIXELS -2:
        neopixels[idx -2] = rgbVal
        neopixels[idx -1] = rgbVal
    time.sleep(0.0125)
    neopixels[idx] = (0, 0, 0)

def rainbowPulse(i):
    for p in range(NUMPIXELS):
        idx = int ((p * 256 / NUMPIXELS) + i)
        neopixels[p] = wheel(idx & 255)

def redPulse():
    aPixel = neopixels[0]
    rCur = aPixel[0]
    gCur = aPixel[1]
    bCur = aPixel[2]

    if DIRECTION == 1:
        neopixels.fill((rCur + 10, gCur, bCur))

    if DIRECTION == 2:
        neopixels.fill((rCur - 10, gCur, bCur))

def whitePulse():
    aPixel = neopixels[0]
    rCur = aPixel[0]
    gCur = aPixel[1]
    bCur = aPixel[2]

    if DIRECTION == 1:
        neopixels.fill((rCur + 10, gCur + 10, bCur + 10))

    if DIRECTION == 2:
        neopixels.fill((rCur - 10, gCur - 10, bCur - 10))

def chase(chaseColor):
    inverseChaseColor = chaseColor
    ## neopixels.fill((0, 0, 0))
    for p in range(NUMPIXELS):
        if inverseChaseColor == 0:
            neopixels[p] = (255, 0, 0)
            inverseChaseColor = 1
        else:
            neopixels[p] = (255, 255, 255)
            inverseChaseColor = 0
        ## print("pixel p should be", p)
        ## print("inverseChaseColor should be: ", inverseChaseColor)
        ## time.sleep(.25)

def kittPulse():
    for p in range(NUMPIXELS):
        neopixels[p] = (255,255,255)
        if p > 2:
            neopixels[p-3] = (255,0,0)
        if p > 7:
            neopixels[p-6] = (0, 0, 0)
        # time.sleep(.015)

######################### MAIN LOOP ##############################

i = 0;
colorChange = 0;
chaseColor = 0;

while True:

    if touch.value:
        neopixels.brightness = 1
        neopixels.fill((0, 0, 0))
        flicker(random.randint(0, (NUMPIXELS-1)),(255, 255, 255))
        colorChange = 1;
        print("D1 touched!")
    else:
        if colorChange:
            colorChange = 0
            # print("Changing color!")
            if COLOR == 1:
                COLOR = 2
            elif COLOR == 2:
                COLOR = 3
            elif COLOR == 3:
                COLOR = 1
            elif COLOR == 4:
                COLOR = 1

            if random.randint(0, 10) == 5:
                COLOR = 4

        aPixel = neopixels[0]
        rCur = aPixel[0]
        # print(rCur)
        if rCur >= 244:
            DIRECTION = 2

        elif rCur <= 50:
            DIRECTION = 1

        if COLOR == 1:
            whitePulse()
            neopixels.brightness = .125
        elif COLOR == 2:
            redPulse()
            neopixels.brightness = .125
        elif COLOR == 3:
            chase(chaseColor)
            if chaseColor == 0:
                chaseColor = 1
            else:
                chaseColor = 0
            neopixels.brightness = .125
        elif COLOR == 4:
            rainbowPulse(i)
            neopixels.brightness = 1

    i = (i+10) % 256  # run from 0 to 255
    time.sleep(.00625) # make bigger to slow down

    # neopixels[0] = (255,255, 255)
    # neopixels[0] = (0, 0, 0)
    # time.sleep(0.1)
