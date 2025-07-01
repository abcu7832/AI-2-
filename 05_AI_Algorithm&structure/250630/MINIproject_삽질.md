# 사물 인식
## 사뮬 = 하리보
* 직접 촬영한 이미지를 이용해 CNN 모델로 학습한 후, OpenCV를 이용해 카메라로 실시간 인식하여 하리보 색깔(클래스) 구분
```python
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

 #모델 및 클래스 정보 불러오기
model = load_model('haribo_color_model(1).h5')  # 학습한 모델 파일명
class_names = ['green', 'middle', 'orange', 'red', 'white', 'yellow']
img_size = (64, 64)  # 학습에 사용한 이미지 크기와 동일해야 함

 #웹캠 열기
cap = cv2.VideoCapture(0)  # 0번 카메라는 기본 웹캠

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 중앙에 사각형 ROI (관심 영역) 표시
    h, w, _ = frame.shape
    size = 200
    x1, y1 = w//2 - size//2, h//2 - size//2
    x2, y2 = x1 + size, y1 + size
    roi = frame[y1:y2, x1:x2]

    # ROI 전처리
    img = cv2.resize(roi, img_size)
    img = img_to_array(img) / 255.
    img = np.expand_dims(img, axis=0)

    # 예측
    pred = model.predict(img)
    class_id = np.argmax(pred)
    class_name = class_names[class_id]
    confidence = np.max(pred)

    # 결과 표시
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    label = f'{class_name} ({confidence:.2f})'
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    cv2.imshow('Haribo Color Classifier', frame)

    # 종료: q 키 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```
* 아직 100% 성공 아님;;;
* 현재 Red, Green, White 세가지만 분류가능하고, 그 외 나머지 색은 아직 불가능.
