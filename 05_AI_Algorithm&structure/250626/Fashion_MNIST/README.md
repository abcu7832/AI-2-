# Fashion MNIST 분류 모델 분석

TensorFlow와 Keras를 이용하여 Fashion MNIST 데이터셋을 학습하고 평가하는 코드

---

## 전체 코드

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score

# 1. 데이터셋 로드 및 분할
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print(train_images.shape)
print(train_labels.shape)
print(test_images.shape)
print(test_labels.shape)

# 클래스 이름 정의
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# 2. 데이터 시각화
matplotlib.use('Qt5Agg')
NUM = 20
plt.figure(figsize=(15,15))
plt.subplots_adjust(hspace=1)
for idx in range(NUM):
    sp = plt.subplot(5,5,idx+1)
    plt.imshow(train_images[idx])
    plt.title(f'{class_names[train_labels[idx]]}')
plt.show()

plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

# 3. 데이터 전처리 (정규화)
train_images = train_images / 255.0
test_images = test_images / 255.0

plt.figure(figsize=(10,8))
for i in range(20):
    plt.subplot(4,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()

# 4. 모델 정의
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax'),
])

model.summary()

# 5. 모델 컴파일 및 학습
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=20)

# 6. 테스트 데이터 예측
predictions = model.predict(test_images)

# 7. 예측 결과 확인
print(f'첫 번째 이미지 예측 클래스: {np.argmax(predictions[0])}')
print(f'첫 번째 이미지 실제 라벨: {test_labels[0]}')

# 8. 결과 시각화 함수 정의
def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                         100*np.max(predictions_array),
                                         class_names[true_label]),
                                         color=color)

def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

# 9. 예측 결과 시각화
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions, test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions, test_labels)
plt.show()

# 10. 최종 정확도 출력
print('accuracy score : ', accuracy_score(tf.math.argmax(predictions, -1), test_labels))

---

## 결과
![train_images](images/train_images.png)
![train_labels](images/train_labels.png)
![test_images](images/test_images.png)
![test_labels](images/test_labels.png)
![accuracy](images/스크린샷 2025-06-26 17-20-10.png)
