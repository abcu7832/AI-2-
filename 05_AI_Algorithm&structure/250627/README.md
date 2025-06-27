# D05 선형모델

## MNIST 실습
* epoch size = 300
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
hist = md.fit(train_x2, train_y, epochs = 300, batch_size = 64, validation_split = 0.2)

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
![images_mnist_학습곡선](/images/250627_d05_mnist학습곡선.png)
![images_mnist_loss](/images/250627_d05_model_loss.png)
