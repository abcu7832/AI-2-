# 사물 인식
## 사물 = 하리보
* 직접 촬영한 이미지를 이용해 CNN 모델로 학습한 후, OpenCV를 이용해 카메라로 실시간 인식하여 하리보 색깔(클래스) 구분
* 이미지 분류 => train, val(validation)
* train: 각 클래스 30개씩
* val: 각 클래스 10개씩
```python
# OpenCV source code
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

 #모델 및 클래스 정보 불러오기
model = load_model('haribo_color_model(1).h5')  # 학습한 모델 파일명
class_names = ['green', 'middle', 'orange', 'red', 'white', 'yellow']
img_size = (64, 64)  # 학습에 사용한 이미지 크기와 동일해야 함

 #웹캠 열기
cap = cv2.VideoCapture(2)  # 2번 카메라는 외부 웹캠

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
```python
# CNN 모델
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
import os

# 경로 설정
train_dir = './haribo_dataset/train'
val_dir = './haribo_dataset/val'

# 이미지 제너레이터 설정 (데이터 증강 포함)
img_size = (64, 64)
batch_size = 16
num_classes = 6  # 클래스 수

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    brightness_range=[0.5, 1.5],
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)  # 검증 데이터는 증강하지 않고 정규화만

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

# CNN 모델 설계 및 학습 - 제너레이터가 성공적으로 생성되었을 경우에만 진행
if train_generator.samples > 0 and val_generator.samples > 0:
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # 학습
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=20
    )

    # 정확도 시각화
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title('Accuracy')
    plt.show()

    # 손실 시각화
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.title('Loss')
    plt.show()
else:
    print("ImageDataGenerator가 이미지를 로드하지 못했습니다. 파일 경로 및 내용 확인이 필요합니다.")
```
* 아직 100% 성공 아님;;;
* 현재 Red, Green, White 세가지만 분류가능하고, 그 외 나머지 색은 아직 불가능.
