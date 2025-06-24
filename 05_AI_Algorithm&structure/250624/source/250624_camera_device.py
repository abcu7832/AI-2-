#import cv2

#cap = cv2.VideoCapture(0)

# 해상도
#w = 640 
#h = 480
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h) 

# 성공적으로 video device 가 열렸으면 while 문 반복
#while(cap.isOpened()):
    # 한 프레임을 읽어옴.
#    ret, frame = cap.read()
#    if ret is False:
#        print("Can't receive frame (stream end?), Exiting ...")
#        break

    # display
   # cv2.imshow("Camera", frame)
    
    # 1ms 동안 대기하여 키 입력받고 q 입력 시 종료
   # key = cv2.waitKey(1)
    #if key & 0xFF == ord('q'):
    #    break

import cv2

cap = cv2.VideoCapture(0)

# 해상도 설정
w = 640
h = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# VideoWriter 객체 생성 (output.mp4로 저장, 30 FPS, MP4V 코덱)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # mp4v 코덱 사용
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (w, h))

while(cap.isOpened()):
    # 한 프레임을 읽어옴
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?), Exiting ...")
        break

    # 프레임을 video 파일로 저장
    out.write(frame)

    # 화면에 프레임 표시
    cv2.imshow("Camera", frame)
    
    # 1ms 동안 대기하여 키 입력받고 'q' 입력 시 종료
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

# 작업 완료 후 객체 해제
cap.release()
out.release()

# 모든 윈도우 닫기
cv2.destroyAllWindows()