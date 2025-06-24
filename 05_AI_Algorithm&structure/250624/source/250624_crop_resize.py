
import cv2

img = cv2.imread("201796967_1280.jpg")

cropped = img[50:450, 100:400]

resized = cv2.resize(cropped, (400,200))

cv2.imshow("Original", img)
cv2.imshow("Cropped image", cropped)
cv2.imshow("Resized image", resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
