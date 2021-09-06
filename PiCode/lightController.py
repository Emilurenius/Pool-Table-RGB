# The original example script that this script is built upon can be found in the same github repository as this file
# Or you can go to the original github repository here: https://github.com/jgarff/rpi_ws281x

import time, json, os, random, datetime, argparse, requests
from rpi_ws281x import *

serverAddress = "http://172.16.4.226:80"

# LED strip configuration:
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def unpackRGB(color): # Change 24 bit color into 8 bit RGB
    r = 0xFF & (color >> 16)
    g = 0xFF & (color >> 8)
    b = 0xFF & color
    return [r, g, b]

def diff(num1, num2):
    if num1 > num2:
        diff = num1 - num2
    else:
        diff = num2 -num1

    return diff

def fadeColor(strip, newColor, wait_ms=10, changePerTick=1):
    oldColor = unpackRGB(strip.getPixelColor(0))
    while True:
        if newColor == oldColor:
            break

        if oldColor[0] == newColor[0]: # Change red channel
            oldColor[0] = newColor[0]
        elif oldColor[0] < newColor[0]:
            oldColor[0] += changePerTick
        elif oldColor[0] > newColor[0]:
            oldColor[0] -= changePerTick
        
        if oldColor[1] == newColor[1]: # Change green channel
            oldColor[1] = newColor[1]
        elif oldColor[1] < newColor[1]:
            oldColor[1] += changePerTick
        elif oldColor[1] > newColor[1]:
            oldColor[1] -= changePerTick
            
        if oldColor[2] == newColor[2]: # Change blue channel
            oldColor[2] = newColor[2]
        elif oldColor[2] < newColor[2]:
            oldColor[2] += changePerTick
        elif oldColor[2] > newColor[2]:
            oldColor[2] -= changePerTick

        solidColor(strip, Color(oldColor[0], oldColor[1], oldColor[2]))
        time.sleep(wait_ms / 1000) # Wait specified amount in delayMS

def solidColor(strip, color):
    # Displays a single solid color untill told otherwise:
    for i in range(strip.numPixels()): # Assign color to every pixel
        strip.setPixelColor(i, color)
    strip.show()

def colorBubbles(strip): 
    stripBrightness = {}

    for i in range(strip.numPixels()):
        stripBrightness[i + 1] = {
            "val": 0,
            "up": True,
            "active": False
        }
    
    while True:
        wait_ms = 50

        noneActive = True
        for i in range(len(stripBrightness)):
            if stripBrightness[i + 1]["active"] == True:
                noneActive = False
                break
        if noneActive:
            stripBrightness[1]["active"] = True

        for i in range(len(stripBrightness)):
            # Fade up
            if stripBrightness[i + 1]["up"] == True and stripBrightness[i + 1]["val"] < 1000 and stripBrightness[i + 1]["active"] == True:
                stripBrightness[i + 1]["val"] += 400
                if stripBrightness[i + 1]["val"] > 1000:
                    stripBrightness[i + 1]["val"] = 1000

            # Fade down
            elif stripBrightness[i + 1]["active"] == True and stripBrightness[i + 1]["val"] > 0:
                stripBrightness[i + 1]["up"] = False
                stripBrightness[i + 1]["val"] -= 100
                if stripBrightness[i + 1]["val"] < 0:
                    stripBrightness[i + 1]["val"] = 0

                if i >= strip.numPixels() - 1:
                    stripBrightness[1]["active"] = True


            else: # Deactivate pixel
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] == 0 and stripBrightness[i + 1]["up"] == False: # Reset pixel
                stripBrightness[i + 1]["up"] = True
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] > 999 and i < len(stripBrightness) - 1: # Activate next pixel
                stripBrightness[i + 2]["active"] = True

            color = Color(int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000))
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def ballDown(strip):
    pointer1 = 0
    pointer2 = strip.numPixels() - 1
    while True:
        strip.setPixelColor(pointer1, Color(255,255,255))
        strip.setPixelColor(pointer2, Color(255,255,255))
        strip.show()
        if diff(pointer1, pointer2) <= 1:
            print("Done")
            break
        else:
            print(diff(pointer1, pointer2))
        time.sleep(0.01)
        pointer1 += 1
        pointer2 -= 1

    repeats = 5
    while repeats > 0:
        solidColor(strip, Color(0, 0, 0))
        time.sleep(0.3)
        solidColor(strip, Color(255, 255, 255))
        time.sleep(0.3)
        repeats -= 1

    fadeColor(strip, [255,0,0])

def ballDown1(strip, origin):
    wait_ms = 10
    pointer1 = origin
    pointer2 = origin - 1

    if pointer2 < 0:
        pointer2 == strip.numPixels() - 1

    stripBrightness = {}
    for i in range(strip.numPixels()):
        stripBrightness[i] = {
            "val": 0,
            "up": True,
            "forwards": True,
            "active": False
        }
    
    stripBrightness[pointer1]["active"] = True
    stripBrightness[pointer2]["active"] = True
    stripBrightness[pointer2]["forwards"] = False

    counter = 0
    animationComplete = False
    while True:
        stillActive = False
        if counter >= 30:
            animationComplete = True

        counter += 1

        for i in range(len(stripBrightness)):
            if stripBrightness[i]["active"] and stripBrightness[i]["up"]:
                stillActive = True
                stripBrightness[i]["val"] += 400
                if stripBrightness[i ]["val"] > 1000:
                    stripBrightness[i]["val"] = 1000
                    stripBrightness[i]["up"] = False

                    if i < len(stripBrightness) - 1 and animationComplete == False and stripBrightness[i]["forwards"]:
                        if i >= strip.numPixels() - 1:
                            stripBrightness[0]["active"] = True
                        else:
                            stripBrightness[i + 1]["active"] = True
                    elif i > 0 and animationComplete == False and stripBrightness[i]["forwards"] == False:
                        print(i)
                        stripBrightness[i - 1]["active"] = True
                        stripBrightness[i - 1]["forwards"] = False

            elif stripBrightness[i]["active"] and stripBrightness[i]["up"] == False:
                if i >= strip.numPixels() - 1:
                    stripBrightness[0]["active"] = True
                stillActive = True
                stripBrightness[i]["val"] -= 50
                if stripBrightness[i ]["val"] < 0:
                    stripBrightness[i]["val"] = 0
                    stripBrightness[i]["active"] = False
                    stripBrightness[i]["up"] = True



            color = Color(int(float(255) * float(stripBrightness[i]["val"]) / 1000), int(float(255) * float(stripBrightness[i]["val"]) / 1000), int(float(255) * float(stripBrightness[i]["val"]) / 1000))
            strip.setPixelColor(i, color)
        
        strip.show()
        if stillActive == False:
            break
        time.sleep(wait_ms/1000)




if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    while True:
        ballsDown = requests.get(f"{serverAddress}/getBallsDown").json()
        if "1" in ballsDown:
            ballDown1(strip, 5)
        time.sleep(0.1)

    