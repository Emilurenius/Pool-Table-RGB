import cv2

img = cv2.imread("resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img,(300,200))
print(imgResize.shape)

imgCropped = img[0:200,200:500]

cv2.imshow("Image", img)
cv2.imshow("Image resize", imgResize)
cv2.imshow("Image cropped", imgCropped)

cv2.waitKey(0)