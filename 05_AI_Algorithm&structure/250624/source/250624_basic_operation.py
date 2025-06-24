import cv2
src = cv2.imread("201796967_1280.jpg",cv2.IMREAD_COLOR)
dst1 = cv2.bitwise_not(src)
dst2 = cv2.bitwise_and(src, src)
dst3 = cv2.bitwise_or(src, src)
dst4 = cv2.bitwise_xor(src, src)
cv2.imshow("src", src)
cv2.imshow("NOT", dst1)
cv2.imshow("AND", dst2)
cv2.imshow("OR", dst3)
cv2.imshow("XOR", dst4)
cv2.waitKey()
cv2.destroyAllWindows()

