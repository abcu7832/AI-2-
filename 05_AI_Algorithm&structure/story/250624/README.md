## 수업내용
* 250623 강의자료 AI.Overview 이어서 진행.
* OpenCV 실습
----------------------------
## OpenCV란?
![OpenCV](/images/250624_1.png)
* opencv: open-source computer vision
* 컴퓨터 비전 관련 작업을 위한 라이브러리 집합
----------------------------
## 개발 환경 설정 -Ubuntu
![OpenCV](/images/250624_2.png)
----------------------------
## 색 체계
![RGB](/images/250624_3.png)
![HSL](/images/250624_4.png)
* HSL 색 검출에 용이함. H에 대해서만 if문을 사용하면 되기 때문
----------------------------
# Basic Operation
## 이미지
![3pHSL](/images/250624_5.png)
* RGB/HSV Color space
```python
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
```
* 원본사진
![3p최형우](/images/250624_6.png)
* bgr
![4p](/images/250624_7.png)
![4p](/images/250624_8.png)
![4p](/images/250624_9.png)
* hsv
![4p](/images/250624_10.png)
![4p](/images/250624_11.png)
![4p](/images/250624_12.png)

* Crop / Resize
---------------------
![4p](/images/250624_13.png)

```python
import cv2

img = cv2.imread("201796967_1280.jpg")

cropped = img[50:450, 100:400]
resized = cv2.resize(cropped, (400,200))

cv2.imshow("Original", img)
cv2.imshow("Cropped image", cropped)
cv2.imshow("Resized image", resized)

cv2.waitKey(0)
cv2.destroyAllWindows()
```
![4p](/images/250624_14.png)


* Reverse Image(역상)
-----------------------------
![4p](/images/250624_15.png)
```python
import cv2

src = cv2.imread("201796967_1280.jpg")
dsdt = cv2.bitwise_not(src)

cv2.imshow("src", src)
cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()
```
![r](/images/250624_16_18_19.png)
![s](/images/250624_17.png)
![d](/images/250624_16_18_19.png)
![e](/images/250624_16_18_19.png)

* Binary
-------------
![5p](/images/250624_21.png)
```python
# bit operation
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
```
![5p](/images/250624_10.png)
* binary(이진화)
![5p](/images/250624_11.png)
```python
import cv2

src = cv2.imread("201796967_1280.jpg", cv2.IMREAD_COLOR)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, dst = cv2.threshold(gray, 100, 100, cv2.THRESH_BINARY)

cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
![5p](/images/250624_11.png)
* edge detection
```python
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
```
* add Weighted
```python
import cv2

src = cv2.imread("201796967_1280.jpg", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

lower_red = cv2.inRange(hsv, (0,100,100),(5,255,255))
upper_red = cv2.inRange(hsv,(170, 200, 200), (180, 255, 255))
added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)

red = cv2.bitwise_and(hsv, hsv, mask = added_red)
red = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)

cv2.imshow("red", red)
cv2.waitKey()
cv2.destroyAllWindows()
```

* 채널 분리 및 병합
```python
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
```

# 카메라&동영상
* 카메라로부터 input을 받아 보여주고 동영상 파일로 저장하기
```python
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
```

* GUI Input 활용하기(TEXT/LINE/RECTANGLE)
```python
import cv2

#비디오 캡처 설정
cap = cv2.VideoCapture(0)

#좌표 설정
topLeft = (50, 50)
bottomRight = (300, 300)

while(cap.isOpened()):
    ret, frame = cap.read()
    #선그리기
    cv2.line(frame, topLeft, bottomRight, (0,255,0), 5)
    #직사각형
    cv2.rectangular(frame, [pt+30 for pt in topLeft], [pt-30 for pt in bottomRight], (0,0,255), 5)

    # 동그라미 그리기
    center = ((topLeft[0] + bottomRight[0]) // 2, (topLeft[1] + bottomRight[1]) // 2)  # 원의 중심
    radius = min(bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]) // 2  # 원의 반지름
    cv2.circle(frame, center, radius, (0, 0, 255), 5)  # 빨간색 동그라미, 두께 5
    
    #텍스트추가
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, '내용', [좌표], font, 텍스트 크기, 색(RGB), 두께)
    cv2.putText(frame, 'BLUR', [pt+80 for pt in topLeft], font, 3, (255, 0, 255), 15)

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

```python
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
```

* GUI Input 활용하기(TRACKBAR)
```python
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
```

```python
import cv2

cap = cv2.VideoCapture(0)

topLeft = (50, 200)
r, g, b = 0, 255, 255  # 초기 색상 설정 (R, G, B)

# 색상 조정 함수
def on_red_trackbar(value):
    global r
    r = value

def on_green_trackbar(value):
    global g
    g = value

def on_blue_trackbar(value):
    global b
    b = value

# 트랙바 창 생성
cv2.namedWindow("Camera")

# 색상 트랙바 (Red, Green, Blue)
cv2.createTrackbar("Red", "Camera", r, 255, on_red_trackbar)
cv2.createTrackbar("Green", "Camera", g, 255, on_green_trackbar)
cv2.createTrackbar("Blue", "Camera", b, 255, on_blue_trackbar)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 글자 색상 설정 (R, G, B 값으로)
    color = (b, g, r)  # OpenCV는 BGR 순서로 색상을 처리

    # 글자 굵기 및 크기 설정
    cv2.putText(frame, "TEXT", topLeft, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

    # 비디오 프레임 출력
    cv2.imshow("Camera", frame)

    # 종료 조건
    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
```
