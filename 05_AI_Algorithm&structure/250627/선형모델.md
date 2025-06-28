# D05 선형모델

## MNIST 실습
* epoch size = 30
```python
# 기본 라이브러리 불러오기
import numpy as np
import pandas as pd

# 데이터셋 불러오기
from tensorflow.keras.datasets import mnist
(train_x, train_y,), (test_x, test_y) = mnist.load_data()

accuracy = hist.history['accuracy']
val_accuracy = hist.history['val_accuracy']  
epoch = np.arange(1, len(accuracy)+1)

# 데이터 확인
train_x.shape, train_y.shape
test_x.shape, test_y.shape 

# 이미지 확인
from PIL import Image
img = train_x[0]

import matplotlib.pyplot as plt
img1 = Image.fromarray(img, mode = 'L')
plt.imshow(img1)

train_y[0]  # 첫번째 데이터 확인

# 데이터 전처리
# 입력 형태 변환: 3차원 -> 2차원: 데이터를 2차원 형태로 변환: 입력 데이터가 선형모델에서는 벡터 형태
train_x1 = train_x.reshape(60000, -1)
test_x1 = test_x.reshape(10000, -1)

# 데이터 값의 크기 조절: 0~1 사이 값으로 변환
train_x2 = train_x1/255
test_x2 = test_x1/255

# 모델 설정
# 모델 설정용 라이브러리 불러오기
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 모델 설정
#md = Sequential()
#md.add(Dense(10, activation = 'softmax', input_shape = (28*28,)))
from tensorflow.keras.layers import Input

md = Sequential()
md.add(Input(shape=(28*28,)))
md.add(Dense(10, activation='softmax'))
md.summary() # 모델 요약

# 모델 학습 진행
# 모델 compile: 손실 함수, 최적화 함수, 측정 함수 설정
#md.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'sgd', metrics = 'acc')
md.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# 모델 학습: 학습 횟수, batch_size, 검증용 데이터 설정
hist = md.fit(train_x2, train_y, epochs = 30, batch_size = 64, validation_split = 0.2)

# Mnist 실습
# 학습결과 분석: 학습 곡선 그리기
plt.figure(figsize = (10, 8))
plt.plot(epoch, accuracy, 'b', label='Training accuracy')
plt.plot(epoch, val_accuracy, 'r', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Mnist 실습
# 테스트용 데이터 평가
md.evaluate(test_x2, test_y)

# 가중치 저장
weight = md.get_weights()
weight

# Model Loss 시각화
plt.plot(hist.history['loss'], label='loss')
plt.plot(hist.history['val_loss'], label='val_loss')
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper right')
plt.show()
```
![images_mnist_모델](/images/250627_d05_model_img.png)
![images_mnist_학습곡선](/images/250627_d05_학습곡선_e30.png)
![images_mnist_loss](/images/250627_d05_loss_e30.png)

## CIFAR10 실습
* MLP
```python
# 기본 라이브러리 불러오기
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# -------------------------------
# CIFAR-10 데이터셋 불러오기
# -------------------------------
from tensorflow.keras.datasets import cifar10
(train_x, train_y), (test_x, test_y) = cifar10.load_data()

# 클래스 이름 정의
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# -------------------------------
# 데이터 전처리
# -------------------------------
train_x_flat = train_x.reshape(50000, -1) / 255.0
test_x_flat = test_x.reshape(10000, -1) / 255.0

# -------------------------------
# 모델 설정 (다층 퍼셉트론)
# -------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model = Sequential([
    Dense(128, activation='relu', input_shape=(32*32*3,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy']
)

# -------------------------------
# 모델 학습
# -------------------------------
hist = model.fit(
    train_x_flat, train_y,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# -------------------------------
# 학습 결과 시각화
# -------------------------------
acc = hist.history['accuracy']
val_acc = hist.history['val_accuracy']
loss = hist.history['loss']
val_loss = hist.history['val_loss']
epochs = np.arange(1, len(acc)+1)

plt.figure(figsize=(10, 6))
plt.plot(epochs, acc, label='Train Accuracy')
plt.plot(epochs, val_acc, label='Validation Accuracy')
plt.title('Training & Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(epochs, loss, label='Train Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# 최종 정확도 및 손실 출력
# -------------------------------
print(f"최종 학습 정확도: {acc[-1]:.4f}")
print(f"최종 검증 정확도: {val_acc[-1]:.4f}")
print(f"최종 학습 손실: {loss[-1]:.4f}")
print(f"최종 검증 손실: {val_loss[-1]:.4f}")

# -------------------------------
# 테스트 평가
# -------------------------------
test_loss, test_acc = model.evaluate(test_x_flat, test_y, verbose=0)
print(f"테스트 정확도: {test_acc:.4f}")
print(f"테스트 손실: {test_loss:.4f}")

# -------------------------------
# 테스트 이미지 하나 예측 + 시각화
# -------------------------------
sample_idx = 0  # 첫 번째 테스트 이미지
sample_img = test_x[sample_idx]
sample_input = test_x_flat[sample_idx].reshape(1, -1)

pred = model.predict(sample_input)
pred_class = np.argmax(pred)

plt.figure(figsize=(3, 3))
plt.imshow(sample_img)
plt.title(f"예측: {class_names[pred_class]} (정답: {class_names[test_y[sample_idx][0]]})")
plt.axis('off')
plt.show()
```
* MLP 기반의 FCNN
```python
# 기본 라이브러리 불러오기
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# -------------------------------
# CIFAR-10 데이터셋 불러오기
# -------------------------------
from tensorflow.keras.datasets import cifar10
(train_x, train_y), (test_x, test_y) = cifar10.load_data()

# 클래스 이름 정의
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# -------------------------------
# 데이터 전처리
# -------------------------------
train_x_flat = train_x.reshape(50000, -1) / 255.0
test_x_flat = test_x.reshape(10000, -1) / 255.0

# -------------------------------
# 모델 설정 (다층 퍼셉트론)
# -------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(128, activation='relu', input_shape=(32*32*3,)),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='sgd',
    metrics=['accuracy']
)

# -------------------------------
# 모델 학습
# -------------------------------
hist = model.fit(
    train_x_flat, train_y,
    epochs=30,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# -------------------------------
# 학습 결과 시각화
# -------------------------------
acc = hist.history['accuracy']
val_acc = hist.history['val_accuracy']
loss = hist.history['loss']
val_loss = hist.history['val_loss']
epochs = np.arange(1, len(acc)+1)

plt.figure(figsize=(10, 6))
plt.plot(epochs, acc, label='Train Accuracy')
plt.plot(epochs, val_acc, label='Validation Accuracy')
plt.title('Training & Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(epochs, loss, label='Train Loss')
plt.plot(epochs, val_loss, label='Validation Loss')
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# 최종 정확도 및 손실 출력
# -------------------------------
print(f"최종 학습 정확도: {acc[-1]:.4f}")
print(f"최종 검증 정확도: {val_acc[-1]:.4f}")
print(f"최종 학습 손실: {loss[-1]:.4f}")
print(f"최종 검증 손실: {val_loss[-1]:.4f}")

# -------------------------------
# 테스트 평가
# -------------------------------
test_loss, test_acc = model.evaluate(test_x_flat, test_y, verbose=0)
print(f"테스트 정확도: {test_acc:.4f}")
print(f"테스트 손실: {test_loss:.4f}")

# -------------------------------
# 테스트 이미지 하나 예측 + 시각화
# -------------------------------
sample_idx = 0  # 첫 번째 테스트 이미지
sample_img = test_x[sample_idx]
sample_input = test_x_flat[sample_idx].reshape(1, -1)

pred = model.predict(sample_input)
pred_class = np.argmax(pred)

plt.figure(figsize=(3, 3))
plt.imshow(sample_img)
plt.title(f"예측: {class_names[pred_class]} (정답: {class_names[test_y[sample_idx][0]]})")
plt.axis('off')
plt.show()
```
