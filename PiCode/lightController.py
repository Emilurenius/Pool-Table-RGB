# The original example script that this script is built upon can be found in the same github repository as this file
# Or you can go to the original github repository here: https://github.com/jgarff/rpi_ws281x

import time, json, os, random, datetime, argparse, requests
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

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
            "forwards": True,
            "active": False
        }

    stripBrightness[1]["active"] = True
    stripBrightness[strip.numPixels() - 1]["active"] = True
    stripBrightness[strip.numPixels() - 1]["forwards"] = False

    while True:
        wait_ms = 50

        for i in range(len(stripBrightness)):

            if stripBrightness[i + 1]["up"] == True and stripBrightness[i + 1]["val"] < 1000 and stripBrightness[i + 1]["active"] == True:
                if stripBrightness[i + 1]["forwards"]:

                    stripBrightness[i + 1]["val"] += 400

                    if stripBrightness[i + 1]["val"] > 1000:
                        stripBrightness[i + 1]["val"] = 1000

                else:
                    stripBrightness[i - 1]["val"] += 400

                    if stripBrightness[i - 1]["val"] > 1000:
                        stripBrightness[i - 1]["val"] = 1000
            
            elif stripBrightness[i + 1]["active"] == True and stripBrightness[i + 1]["val"] > 0:
                if stripBrightness[i + 1]["forwards"]:

                    stripBrightness[i + 1]["up"] = False
                    stripBrightness[i + 1]["val"] -= 100

                    if stripBrightness[i + 1]["val"] < 0:
                        stripBrightness[i + 1]["val"] = 0

                else:
                    stripBrightness[i - 1]["up"] = False
                    stripBrightness[i - 1]["val"] -= 100

                    if stripBrightness[i - 1]["val"] < 0:
                        stripBrightness[i - 1]["val"] = 0

                    if i >= strip.numPixels() - 1 and stripBrightness[i + 1]["forwards"] == True:
                        stripBrightness[1]["active"] = True
                    elif i >= strip.numPixels() - 1 and stripBrightness[i + 1]["forwards"] == False:
                        stripBrightness[strip.numPixels() - 1]["active"] = True
                        stripBrightness[strip.numPixels() - 1]["forwards"] = False

            else: # Deactivate pixel
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] == 0 and stripBrightness[i + 1]["up"] == False: # Reset pixel
                stripBrightness[i + 1]["up"] = True
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] > 999 and i < len(stripBrightness) - 1: # Activate next pixel
                if stripBrightness[i + 1]["forwards"]:
                    stripBrightness[i + 2]["active"] = True
                else:
                    stripBrightness[i - 2]["active"] = True
                

            color = Color(int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000))
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


    
    # while True:
    #     wait_ms = 50

    #     for i in range(len(stripBrightness)):
    #         #print(f"{i} : {strip.numPixels()}")
            
    #         # Fade up
    #         if stripBrightness[i + 1]["up"] == True and stripBrightness[i + 1]["val"] < 1000 and stripBrightness[i + 1]["active"] == True:
    #             stripBrightness[i + 1]["val"] += 400
    #             if stripBrightness[i + 1]["val"] > 1000:
    #                 stripBrightness[i + 1]["val"] = 1000

    #         # Fade down
    #         elif stripBrightness[i + 1]["active"] == True and stripBrightness[i + 1]["val"] > 0:
    #             stripBrightness[i + 1]["up"] = False
    #             stripBrightness[i + 1]["val"] -= 100
    #             if stripBrightness[i + 1]["val"] < 0:
    #                 stripBrightness[i + 1]["val"] = 0

    #             if i >= strip.numPixels() - 1:
    #                 stripBrightness[1]["active"] = True
    #                 print("It's working")

            # else: # Deactivate pixel
            #     stripBrightness[i + 1]["active"] = False

    #         if stripBrightness[i + 1]["val"] == 0 and stripBrightness[i + 1]["up"] == False: # Reset pixel
    #             stripBrightness[i + 1]["up"] = True
    #             stripBrightness[i + 1]["active"] = False

    #         if stripBrightness[i + 1]["val"] > 999 and i < len(stripBrightness) - 1: # Activate next pixel
    #             if stripBrightness[i + 1]["forwards"]:
    #                 stripBrightness[i + 2]["active"] = True
    #             else:
    #                 stripBrightness[i - 2]["active"] = True


    #         color = Color(int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000))
    #         strip.setPixelColor(i, color)
    #     strip.show()
    #     time.sleep(wait_ms/1000.0)

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
        colorBubbles(strip)

    