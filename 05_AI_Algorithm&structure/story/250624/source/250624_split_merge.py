import numpy as np
import cv2

src = cv2.imread("201796967_1280.jpg", cv2.IMREAD_COLOR)
b, g, r = cv2.split(src)
inverse = cv2.merge((r, g, b))

cv2.imshow("b", b)
cv2.imshow("g", g)
cv2.imshow("r", r)
cv2.imshow("inverse", inverse)

b = src[:, :, 0]
g = src[:, :, 1]
r = src[:, :, 2]
height, width, channel = src.shape
zero = np.zeros((height, width, 1), dtype=np.uint8)
bgz = cv2.merge((b, g, zero))

cv2.imshow("bgz", bgz)

cv2.waitKey()
cv2.destroyAllWindows()
