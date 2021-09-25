# The original example script that this script is built upon can be found in the same github repository as this file
# Or you can go to the original github repository here: https://github.com/jgarff/rpi_ws281x

import time, json, os, random, datetime, argparse, requests
from rpi_ws281x import *

serverAddress = "http://localhost:3000"
holesPos = [20, 40, 80, 100, 120, 140]

# LED strip configuration:
LED_COUNT      = 144     # Number of LED pixels.
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
    LEDdata = {}

    for i in range(strip.numPixels()):
        LEDdata[i + 1] = {
            "val": 0,
            "up": True,
            "active": False
        }
    
    while True:
        wait_ms = 50

        noneActive = True
        for i in range(len(LEDdata)):
            if LEDdata[i + 1]["active"] == True:
                noneActive = False
                break
        if noneActive:
            LEDdata[1]["active"] = True

        for i in range(len(LEDdata)):
            # Fade up
            if LEDdata[i + 1]["up"] == True and LEDdata[i + 1]["val"] < 1000 and LEDdata[i + 1]["active"] == True:
                LEDdata[i + 1]["val"] += 400
                if LEDdata[i + 1]["val"] > 1000:
                    LEDdata[i + 1]["val"] = 1000

            # Fade down
            elif LEDdata[i + 1]["active"] == True and LEDdata[i + 1]["val"] > 0:
                LEDdata[i + 1]["up"] = False
                LEDdata[i + 1]["val"] -= 100
                if LEDdata[i + 1]["val"] < 0:
                    LEDdata[i + 1]["val"] = 0

                if i >= strip.numPixels() - 1:
                    LEDdata[1]["active"] = True


            else: # Deactivate pixel
                LEDdata[i + 1]["active"] = False

            if LEDdata[i + 1]["val"] == 0 and LEDdata[i + 1]["up"] == False: # Reset pixel
                LEDdata[i + 1]["up"] = True
                LEDdata[i + 1]["active"] = False

            if LEDdata[i + 1]["val"] > 999 and i < len(LEDdata) - 1: # Activate next pixel
                LEDdata[i + 2]["active"] = True

            color = Color(int(float(255) * float(LEDdata[i + 1]["val"]) / 1000), int(float(255) * float(LEDdata[i + 1]["val"]) / 1000), int(float(255) * float(LEDdata[i + 1]["val"]) / 1000))
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

    LEDdata = {}
    for i in range(strip.numPixels()):
        LEDdata[i] = {
            "val": 100,
            "up": True,
            "forwards": True,
            "active": False
        }
    
    LEDdata[pointer1]["active"] = True
    LEDdata[pointer2]["active"] = True
    LEDdata[pointer2]["forwards"] = False

    counter = 0
    animationComplete = False
    while True:
        stillActive = False
        if counter >= 30:
            animationComplete = True

        counter += 1

        for i in range(len(LEDdata)):

            if LEDdata[i]["active"] and LEDdata[i]["up"]: # Fade up
                stillActive = True
                LEDdata[i]["val"] += 400
                if LEDdata[i ]["val"] > 1000:
                    LEDdata[i]["val"] = 1000
                    LEDdata[i]["up"] = False

                    if i < len(LEDdata) - 1 and animationComplete == False and LEDdata[i]["forwards"]: # Activate next LED
                        if i >= strip.numPixels() - 1:
                            LEDdata[0]["active"] = True
                        else:
                            LEDdata[i + 1]["active"] = True
                    elif i > 0 and animationComplete == False and LEDdata[i]["forwards"] == False: # Activate next LED
                        print(i)
                        LEDdata[i - 1]["active"] = True
                        LEDdata[i - 1]["forwards"] = False

            elif LEDdata[i]["active"] and LEDdata[i]["up"] == False: # fade down
                if i >= strip.numPixels() - 1 and LEDdata[i]["forwards"]:
                    LEDdata[0]["active"] = True
                elif i <= 1 and LEDdata[i]["forwards"] == False:
                    print("Looping backwards")
                    LEDdata[strip.numPixels() - 1]["active"] = True
                    LEDdata[strip.numPixels() - 1]["forwards"] = False
                    
                stillActive = True
                LEDdata[i]["val"] -= 50
                if LEDdata[i ]["val"] < 100: # Reset pixel
                    LEDdata[i]["val"] = 100
                    LEDdata[i]["active"] = False
                    LEDdata[i]["up"] = True


            background = Color(int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(0) * float(LEDdata[i]["val"]) / 1000), int(float(0) * float(LEDdata[i]["val"]) / 1000))
            animationColor = Color(int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(255) * float(LEDdata[i]["val"]) / 1000))
            if LEDdata[i]["active"]:
                strip.setPixelColor(i, animationColor)
            else:
                strip.setPixelColor(i, background)
        
        strip.show()
        if stillActive == False:
            break
        time.sleep(wait_ms/1000)

def animateHoles(strip, wait_ms=10, steps=30):
    holeStates = [False, False, False, False, False, False]

    LEDdata = {}
    for i in range(strip.numPixels()):
        LEDdata[i] = {
            "val": 100,
            "step": 0, # Used to check how many LEDs have been lit up since the animation started
            "up": True,
            "forwards": True,
            "active": False
        }

    while True:
        ballsDown = requests.get(f"{serverAddress}/getBallsDown").json()

        for ball in ballsDown:
            holeStates[int(ball)] = True

        i = 0
        for state in holeStates:
            if state:
                LEDdata[holesPos[i]]["active"] = True
                if i <=0: # Make sure values are within range
                    LEDdata[strip.numPixels() - 1]["active"] = True
                    LEDdata[strip.numPixels() - 1]["forwards"] = False
                else:
                    LEDdata[holesPos[i]-1]["active"] = True
                    LEDdata[holesPos[i]-1]["forwards"] = False
            i += 1

        for i in range(len(LEDdata)):
            if LEDdata[i]["active"] and LEDdata[i]["up"]: # Fade up
                LEDdata[i]["val"] += 400
                if LEDdata[i ]["val"] > 1000:
                    LEDdata[i]["val"] = 1000
                    LEDdata[i]["up"] = False

                    if i < len(LEDdata) - 1 and LEDdata[i]["forwards"] and LEDdata[i]["step"] < steps: # Activate next LED
                        print(f"{i}: {LEDdata[i]['step']}")
                        if i >= strip.numPixels() - 1:
                            LEDdata[0]["active"] = True
                            LEDdata[0]["step"] = LEDdata[i]["step"] + 1
                        else:
                            LEDdata[i + 1]["active"] = True
                            LEDdata[i + 1]["step"] = LEDdata[i]["step"] + 1
                    elif i > 0 and LEDdata[i]["forwards"] == False and LEDdata[i]["step"] < steps: # Activate next LED
                        LEDdata[i - 1]["active"] = True
                        LEDdata[i - 1]["forwards"] = False
                        LEDdata[i - 1]["step"] = LEDdata[i]["step"] + 1

            elif LEDdata[i]["active"] and LEDdata[i]["up"] == False: # Fade down
                if i >= strip.numPixels() - 1 and LEDdata[i]["forwards"]:
                    LEDdata[0]["active"] = True
                elif i <= 1 and LEDdata[i]["forwards"] == False:
                    print("Looping backwards")
                    LEDdata[strip.numPixels() - 1]["active"] = True
                    LEDdata[strip.numPixels() - 1]["forwards"] = False
                    
                LEDdata[i]["val"] -= 50
                if LEDdata[i ]["val"] < 100: # Reset pixel
                    LEDdata[i]["val"] = 100
                    LEDdata[i]["active"] = False
                    LEDdata[i]["up"] = True

            background = Color(int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(0) * float(LEDdata[i]["val"]) / 1000), int(float(0) * float(LEDdata[i]["val"]) / 1000))
            animationColor = Color(int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(255) * float(LEDdata[i]["val"]) / 1000), int(float(255) * float(LEDdata[i]["val"]) / 1000))
            if LEDdata[i]["active"]:
                strip.setPixelColor(i, animationColor)
            else:
                strip.setPixelColor(i, background)
        
        strip.show()
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

    # while True:
    #     ballsDown = requests.get(f"{serverAddress}/getBallsDown").json()

    #     for ball in ballsDown:
    #         ballDown1(strip, holesPos[int(ball)])
    #     time.sleep(0.1)

    animateHoles(strip)

else:
    print(__name__)

    