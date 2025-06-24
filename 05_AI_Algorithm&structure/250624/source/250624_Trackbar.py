import cv2

cap = cv2.VideoCapture(0)

topLeft = (50,200)
bold = 0

def on_bold_trackbar(value):
    global bold
    bold = value

cv2.namedWindow("Camera")
cv2.createTrackbar("bold", "Camera", bold, 10, on_bold_trackbar)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 굵기 변경
    #cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255,255), 1+bold)
    # font size 변경
    cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2 + bold, (0, 255,255), 1)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
#
##import cv2
#
##cap = cv2.VideoCapture(0)
#
##topLeft = (50, 200)
##r, g, b = 0, 255, 255  # 초기 색상 설정 (R, G, B)
#
## 색상 조정 함수
##def on_red_trackbar(value):
#    #global r
#    #r = value
#
##def on_green_trackbar(value):
#    #global g
#    #g = value
#
#def on_blue_trackbar(value):
#    global b
#    b = value
#
## 트랙바 창 생성
#cv2.namedWindow("Camera")
#
## 색상 트랙바 (Red, Green, Blue)
#cv2.createTrackbar("Red", "Camera", r, 255, on_red_trackbar)
#cv2.createTrackbar("Green", "Camera", g, 255, on_green_trackbar)
#cv2.createTrackbar("Blue", "Camera", b, 255, on_blue_trackbar)
#
#while(cap.isOpened()):
#    ret, frame = cap.read()
#    if ret is False:
#        print("Can't receive frame (stream end?). Exiting ...")
#        break
#
#    # 글자 색상 설정 (R, G, B 값으로)
#    color = (b, g, r)  # OpenCV는 BGR 순서로 색상을 처리
#
#    # 글자 굵기 및 크기 설정
#    cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)
#
#    # 비디오 프레임 출력
#    cv2.imshow("Camera", frame)
#
#    # 종료 조건
#    key = cv2.waitKey(30) & 0xFF
#    if key == ord('q'):
#        break
#
## 자원 해제
#cap.release()
#cv2.destroyAllWindows()
