import time, RPi.GPIO as GPIO, requests, random

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.setup(12, GPIO.OUT)

while True:
    time.sleep(0.1)
    GPIO.output(12, False)

    if (GPIO.input(16)):
        print("Ball detected!")
        GPIO.output(12, True)
        
        hole = random.randint(0, 5)
        requests.get(f"http://172.16.4.195:3000/balldown?hole={hole}")
        print(hole, "Activated")