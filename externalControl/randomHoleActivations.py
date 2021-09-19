import time, requests, random

while True:
    time.sleep(random.randint(1, 5))
    hole = random.randint(0, 5)
    requests.get(f"http://172.16.4.195:3000/balldown?hole={hole}")
    print(hole, "Activated")
