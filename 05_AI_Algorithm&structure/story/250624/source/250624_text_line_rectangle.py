import cv2

#비디오 캡처 설정
#cap = cv2.VideoCapture(0)

#좌표 설정
#topLeft = (50, 50)
#bottomRight = (300, 300)

#while(cap.isOpened()):
 #   ret, frame = cap.read()
    #선그리기
  #  cv2.line(frame, topLeft, bottomRight, (0,255,0), 5)
    #직사각형
    #cv2.rectangular(frame, [pt+30 for pt in topLeft], [pt-30 for pt in bottomRight], (0,0,255), 5)

    # 동그라미 그리기
   # center = ((topLeft[0] + bottomRight[0]) // 2, (topLeft[1] + bottomRight[1]) // 2)  # 원의 중심
    #radius = min(bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]) // 2  # 원의 반지름
    #cv2.circle(frame, center, radius, (0, 0, 255), 5)  # 빨간색 동그라미, 두께 5
    
    #텍스트추가
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame, '내용', [좌표], font, 텍스트 크기, 색(RGB), 두께)
    #cv2.putText(frame, 'BLUR', [pt+80 for pt in topLeft], font, 3, (255, 0, 255), 15)

    #cv2.imshow("Camera", frame)

    #key = cv2.waitKey(30) & 0xFF
    #if key == ord("q"):
    #    break

#cap.release()
#cv2.destroyAllWindows()

import cv2

# 마우스 클릭 위치를 저장할 리스트
circle_centers = []

# 마우스 클릭 이벤트 처리 함수
def mouse_callback(event, x, y, flags, param):
    global circle_centers
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭 시
        circle_centers.append((x, y))  # 클릭한 위치를 리스트에 추가

# 비디오 캡처 설정
cap = cv2.VideoCapture(0)

# 좌표 설정
topLeft = (50, 50)
bottomRight = (300, 300)

# 마우스 콜백 함수 등록
cv2.namedWindow("Camera")
cv2.setMouseCallback("Camera", mouse_callback)

while(cap.isOpened()):
    ret, frame = cap.read()

    # 선 그리기
    cv2.line(frame, topLeft, bottomRight, (0, 255, 0), 5)

    # 직사각형 대신 동그라미 그리기
    center = ((topLeft[0] + bottomRight[0]) // 2, (topLeft[1] + bottomRight[1]) // 2)
    radius = min(bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]) // 2
    cv2.circle(frame, center, radius, (0, 0, 255), 5)

    # 텍스트 추가
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, 'BLUR', [pt + 80 for pt in topLeft], font, 3, (255, 0, 255), 15)

    # 마우스 클릭으로 추가된 동그라미 그리기
    for (cx, cy) in circle_centers:
        cv2.circle(frame, (cx, cy), 30, (0, 255, 0), 5)  # 클릭한 위치에 동그라미

    # 비디오 창에 출력
    cv2.imshow("Camera", frame)

    # 종료 조건
    key = cv2.waitKey(30) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
