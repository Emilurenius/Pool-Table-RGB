import time, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

while True:
    time.sleep(0.1)
    GPIO.output(12, False)

    if (GPIO.input(16)):
        print("Ball detected!")
        GPIO.output(12, True)