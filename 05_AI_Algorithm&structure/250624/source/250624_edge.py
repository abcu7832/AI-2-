import cv2

src = cv2.imread("201796967_1280.jpg", cv2.IMREAD_COLOR)
#gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(src, 100, 200)
#laplacian = cv2.Laplacian(src, cv2.CV_64F)
#laplacian_abs = cv2.convertScaleAbs(laplacian)
#sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 3)

cv2.imshow("Canny", edges)
#cv2.imshow("sobel", sobel)
#cv2.imshow('Original Image', src)
#cv2.imshow('Laplacian Image', laplacian_abs)

cv2.waitKey()
cv2.destroyAllWindows()
