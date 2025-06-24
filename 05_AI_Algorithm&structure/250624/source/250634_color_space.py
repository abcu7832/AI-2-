import numpy as np
import cv2

#이미지 파일을 READ하고 color space 정보 출력
color = cv2.imread("201796967_1280.jpg", cv2.IMREAD_COLOR)
#color = cv2.imread("strawberry_dark.jpg", cv2.IMREAD_COLOR)
print(color.shape)

height,width,channels = color.shape
cv2.imshow("Original Image", color)

#color channel 을 RGB로 분할하여 출력
b,g,r = cv2.split(color)
rgb_split = np.concatenate((b,g,r),axis=1)
cv2.imshow("BGR channels", rgb_split)

# 색공간을 bgr에서 HSV로 변환
hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)

# channel 을 HSV로 분할하여 출력
h,s,v = cv2.split(hsv)
hsv_split = np.concatenate((h,s,v),axis=1)
cv2.imshow("split HSV", hsv_split)

cv2.waitKey(0)

cv2.imwrite("output.png", img)

cv2.destroyAllwindows()
