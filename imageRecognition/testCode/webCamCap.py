import cv2, numpy as np

print("Imported module")

try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)


print("Camera accessed\nStarting in:")
cap.set(3,640)
print("3")
cap.set(4,480)
print("2")
cap.set(10,100)
print("1")

while True:
    success, img = cap.read()
    print(success)
    if success:
        cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break