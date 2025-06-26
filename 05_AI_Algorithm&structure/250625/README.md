# 퍼셉트론 python 코드

## 단층 퍼셉트론으로 AND gate를 시뮬레이션하기 위한 코드
```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=10):
        self.weights = np.zeros(input_size)
        self.bias = 0 
        self.lr = lr
        self.epochs = epochs
        self.errors = []

    def activation(self, x):
        return np.where(x > 0, 1, 0)  # 올바른 이진 계단 함수

    def predict(self, x):
        linear_output = np.dot(x, self.weights) + self.bias
        return self.activation(linear_output)

    def train(self, x, y):
        for epoch in range(self.epochs):
            total_error = 0
            for xi, target in zip(x, y):
                prediction = self.predict(xi)
                update = self.lr * (target - prediction)
                self.weights += update * xi
                self.bias += update
                total_error += abs(target - prediction)
            self.errors.append(total_error)
            print(f"Epoch {epoch+1}/{self.epochs}, Errors: {total_error}")

# AND 게이트 데이터
x_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])

# 퍼셉트론 모델 훈련
ppn_and = Perceptron(input_size=2)
ppn_and.train(x_and, y_and)

# 예측 결과 확인
print("\nAND GATE TEST:")
for x in x_and:
    print(f"Input: {x}, Predicted Output: {ppn_and.predict(x)}")

from matplotlib.colors import ListedColormap

def plot_decision_boundary(X, y, model):
  cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
  cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

  h = .02 # mesh grid 간격
  x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  y_min, y_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

  Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)

  plt.figure()
  plt.contourf(xx, yy, Z, cmap=cmap_light)

  # 실제 데이터 포인트 표시
  plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=100, marker = 'o')
  plt.xlabel('Input 1') 
  plt.ylabel('Input 2') 
  plt.title('Perceptron Decision Boundary')
  plt.show()

# AND 게이트 결정 경계 시각화
plot_decision_boundary(x_and, y_and, ppn_and)

# 오류 시각화
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(ppn_and.errors) + 1), ppn_and.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of Errors')
plt.title('Perceptron Learning Error Over Epochs (AND Gate)')
plt.grid(True)
plt.show()
```
![AND_result](/images/250625_AND_r.png)
![AND_boundary](/images/250625_AND_b.png)
![AND_error](/images/250625_AND_e.png)

## 단층 퍼셉트론으로 OR gate를 시뮬레이션하기 위한 코드
```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=10):
        self.weights = np.zeros(input_size)
        self.bias = 0 
        self.lr = lr
        self.epochs = epochs
        self.errors = []

    def activation(self, x):
        return np.where(x > 0, 1, 0)  # 올바른 이진 계단 함수

    def predict(self, x):
        linear_output = np.dot(x, self.weights) + self.bias
        return self.activation(linear_output)

    def train(self, x, y):
        for epoch in range(self.epochs):
            total_error = 0
            for xi, target in zip(x, y):
                prediction = self.predict(xi)
                update = self.lr * (target - prediction)
                self.weights += update * xi
                self.bias += update
                total_error += abs(target - prediction)
            self.errors.append(total_error)
            print(f"Epoch {epoch+1}/{self.epochs}, Errors: {total_error}")

# OR 게이트 데이터
x_or = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_or = np.array([0, 1, 1, 1])

# 퍼셉트론 모델 훈련
ppn_or = Perceptron(input_size=2)
ppn_or.train(x_or, y_or)

# 예측 결과 확인
print("\nOR GATE TEST:")
for x in x_or:
    print(f"Input: {x}, Predicted Output: {ppn_or.predict(x)}")

from matplotlib.colors import ListedColormap

def plot_decision_boundary(X, y, model):
  cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
  cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

  h = .02 # mesh grid 간격
  x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  y_min, y_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

  Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)

  plt.figure()
  plt.contourf(xx, yy, Z, cmap=cmap_light)

  # 실제 데이터 포인트 표시
  plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=100, marker = 'o')
  plt.xlabel('Input 1') 
  plt.ylabel('Input 2') 
  plt.title('Perceptron Decision Boundary')
  plt.show()

# AND 게이트 결정 경계 시각화
plot_decision_boundary(x_or, y_or, ppn_or)

# 오류 시각화
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(ppn_or.errors) + 1), ppn_or.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of Errors')
plt.title('Perceptron Learning Error Over Epochs (OR Gate)')
plt.grid(True)
plt.show()
```
![or_result](/images/250625_or_r.png)
![or_boundary](/images/250625_or_b.png)
![or_error](/images/250625_or_e.png)

## 단층 퍼셉트론으로 NAND gate를 시뮬레이션하기 위한 코드
```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=10):
        self.weights = np.zeros(input_size)
        self.bias = 0 
        self.lr = lr
        self.epochs = epochs
        self.errors = []

    def activation(self, x):
        return np.where(x > 0, 1, 0)  # 올바른 이진 계단 함수

    def predict(self, x):
        linear_output = np.dot(x, self.weights) + self.bias
        return self.activation(linear_output)

    def train(self, x, y):
        for epoch in range(self.epochs):
            total_error = 0
            for xi, target in zip(x, y):
                prediction = self.predict(xi)
                update = self.lr * (target - prediction)
                self.weights += update * xi
                self.bias += update
                total_error += abs(target - prediction)
            self.errors.append(total_error)
            print(f"Epoch {epoch+1}/{self.epochs}, Errors: {total_error}")

# NAND 게이트 데이터
x_nand = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_nand = np.array([1, 0, 0, 0])

# 퍼셉트론 모델 훈련
ppn_nand = Perceptron(input_size=2)
ppn_nand.train(x_nand, y_nand)

# 예측 결과 확인
print("\nNAND GATE TEST:")
for x in x_nand:
    print(f"Input: {x}, Predicted Output: {ppn_nand.predict(x)}")

from matplotlib.colors import ListedColormap

def plot_decision_boundary(X, y, model):
  cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
  cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

  h = .02 # mesh grid 간격
  x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  y_min, y_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

  Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)

  plt.figure()
  plt.contourf(xx, yy, Z, cmap=cmap_light)

  # 실제 데이터 포인트 표시
  plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=100, marker = 'o')
  plt.xlabel('Input 1') 
  plt.ylabel('Input 2') 
  plt.title('Perceptron Decision Boundary')
  plt.show()

# NAND 게이트 결정 경계 시각화
plot_decision_boundary(x_nand, y_nand, ppn_nand)

# 오류 시각화
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(ppn_nand.errors) + 1), ppn_nand.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of Errors')
plt.title('Perceptron Learning Error Over Epochs (NAND Gate)')
plt.grid(True)
plt.show()
```
![NAND_result](/images/250625_nand_r.png)
![NAND_boundary](/images/250625_nand_b.png)
![NAND_error](/images/250625_nand_e.png)
## 단층 퍼셉트론으로 XOR gate를 시뮬레이션하기 위한 코드
```python
import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, lr=0.1, epochs=10):
        self.weights = np.zeros(input_size)
        self.bias = 0 
        self.lr = lr
        self.epochs = epochs
        self.errors = []

    def activation(self, x):
        return np.where(x > 0, 1, 0)  # 올바른 이진 계단 함수

    def predict(self, x):
        linear_output = np.dot(x, self.weights) + self.bias
        return self.activation(linear_output)

    def train(self, x, y):
        for epoch in range(self.epochs):
            total_error = 0
            for xi, target in zip(x, y):
                prediction = self.predict(xi)
                update = self.lr * (target - prediction)
                self.weights += update * xi
                self.bias += update
                total_error += abs(target - prediction)
            self.errors.append(total_error)
            print(f"Epoch {epoch+1}/{self.epochs}, Errors: {total_error}")

# XOR 게이트 데이터
x_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

# 퍼셉트론 모델 훈련
ppn_xor = Perceptron(input_size=2)
ppn_xor.train(x_xor, y_xor)

# 예측 결과 확인
print("\nXOR GATE TEST:")
for x in x_xor:
    print(f"Input: {x}, Predicted Output: {ppn_xor.predict(x)}")

from matplotlib.colors import ListedColormap

def plot_decision_boundary(X, y, model):
  cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
  cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

  h = .02 # mesh grid 간격
  x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  y_min, y_max = X[:, 0].min() - 1, X[:, 0].max() + 1
  xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

  Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
  Z = Z.reshape(xx.shape)

  plt.figure()
  plt.contourf(xx, yy, Z, cmap=cmap_light)

  # 실제 데이터 포인트 표시
  plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, edgecolor='k', s=100, marker = 'o')
  plt.xlabel('Input 1') 
  plt.ylabel('Input 2') 
  plt.title('Perceptron Decision Boundary')
  plt.show()

# NAND 게이트 결정 경계 시각화
plot_decision_boundary(x_xor, y_xor, ppn_xor)

# 오류 시각화
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(ppn_xor.errors) + 1), ppn_xor.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Number of Errors')
plt.title('Perceptron Learning Error Over Epochs (XOR Gate)')
plt.grid(True)
plt.show()

```
![xor_result](/images/250625_xor_r.png)
![xor_boundary](/images/250625_xor_b.png)
![xor_error](/images/250625_xor_e.png)
## 다중 퍼셉트론으로 XOR gate를 시뮬레이션하기 위한 코드
```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 시그모이드 함수 및 도함수
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# XOR 데이터
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

# 시드 고정
np.random.seed(42)

# 신경망 구조
input_size = 2
hidden_size = 4
output_size = 1
lr = 0.1
epochs = 10000

# 가중치 및 바이어스 초기화
w1 = np.random.randn(input_size, hidden_size)
b1 = np.zeros((1, hidden_size))
w2 = np.random.randn(hidden_size, output_size)
b2 = np.zeros((1, output_size))

loss_history = []

# 학습
for epoch in range(epochs):
    # 순전파
    z1 = np.dot(X, w1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, w2) + b2
    y_pred = sigmoid(z2)

    # 손실 계산
    loss = np.mean((y - y_pred)**2)
    loss_history.append(loss)

    # 역전파
    d_loss_y = 2 * (y_pred - y)
    d_output = d_loss_y * sigmoid_derivative(y_pred)
    d_hidden = np.dot(d_output, w2.T) * sigmoid_derivative(a1)

    # 가중치 업데이트
    w2 -= lr * np.dot(a1.T, d_output)
    b2 -= lr * np.sum(d_output, axis=0, keepdims=True)
    w1 -= lr * np.dot(X.T, d_hidden)
    b1 -= lr * np.sum(d_hidden, axis=0, keepdims=True)

    # 로그 출력
    if (epoch + 1) % 1000 == 0 or epoch == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss:.6f}")

# 최종 출력 확인
print("\nXOR 테스트 결과:")
for i in range(4):
    print(f"Input: {X[i]}, Predicted: {y_pred[i][0]:.4f}, Rounded: {round(y_pred[i][0])}")

# 결정 경계 시각화
def plot_decision_boundary(X, y, model_func, resolution=0.01):
    cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF'])
    cmap_bold = ListedColormap(['#FF0000', '#0000FF'])

    x_min, x_max = X[:,0].min() - 0.5, X[:,0].max() + 0.5
    y_min, y_max = X[:,1].min() - 0.5, X[:,1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, resolution),
                         np.arange(y_min, y_max, resolution))

    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = model_func(grid)
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(6,6))
    plt.contourf(xx, yy, Z, cmap=cmap_light)
    plt.scatter(X[:,0], X[:,1], c=y.ravel(), cmap=cmap_bold, edgecolor='k', s=100)
    plt.title("MLP Decision Boundary for XOR")
    plt.xlabel("Input 1")
    plt.ylabel("Input 2")
    plt.grid(True)
    plt.show()

# 모델 예측 함수 (결정 경계용)
def mlp_predict(x_input):
    a1 = sigmoid(np.dot(x_input, w1) + b1)
    out = sigmoid(np.dot(a1, w2) + b2)
    return (out > 0.5).astype(int)

# 시각화 실행
plot_decision_boundary(X, y, mlp_predict)

# 🔴 손실 그래프 시각화
plt.figure(figsize=(8,5))
plt.plot(loss_history)
plt.title("Loss over Epochs (XOR MLP)")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.grid(True)
plt.show()
```
![xor_result](/images/250625_xor_mr.png)
![xor_boundary](/images/250625_xor_mb.png)
![xor_error](/images/250625_xor_me.png)
