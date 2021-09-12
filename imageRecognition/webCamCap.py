import cv2, numpy as np
kernel = np.ones((5,5),np.uint8)

print("Imported module")
cap = cv2.VideoCapture(0)
print("Camera accessed\nStarting in:")
cap.set(3,640)
print("3")
cap.set(4,480)
print("2")
cap.set(10,100)
print("1")

while True:
    success, img = cap.read()
    imgCanny = cv2.Canny(img,100,100)
    imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
    imgEroded = cv2.erode(imgDialation,kernel,iterations=1)
    cv2.imshow("Video",imgEroded)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break