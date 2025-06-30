# CNN 실습
## 
```python
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def conv(a, b):
    c = np.array(a) * np.array(b)
    return np.sum(c)

def MaxPooling(nimg):
    nimg = np.array(nimg)
    i0, j0 = nimg.shape
    if i0 % 2 == 1:
        nimg = np.vstack([nimg, np.zeros((1, j0))])
    if j0 % 2 == 1:
        nimg = np.hstack([nimg, np.zeros((nimg.shape[0], 1))])

    output = np.zeros((nimg.shape[0] // 2, nimg.shape[1] // 2))
    for i in range(output.shape[0]):
        for j in range(output.shape[1]):
            a = nimg[2*i:2*i+2, 2*j:2*j+2]
            output[i, j] = a.max()
    return output

def featuring(nimg, filt):
    feature = np.zeros((nimg.shape[0]-2, nimg.shape[1]-2))
    for i in range(feature.shape[0]):
        for j in range(feature.shape[1]):
            a = nimg[i:i+3, j:j+3]
            feature[i, j] = conv(a, filt)
    return feature

def Pooling(nimg):
    return [MaxPooling(f) for f in nimg]

def to_img(nimg):
    nimg = np.array(nimg)
    nimg = np.uint8(np.clip(np.round(nimg), 0, 255))
    return [Image.fromarray(nimg[i]) for i in range(len(nimg))]

# ✅ filters를 인자로 받도록 수정
def ConvD(nimg, filters):
    return [featuring(nimg, f) for f in filters]

def ReLU(f0):
    return [np.maximum(f, 0) for f in f0]

def Softmax(f0):
    return [np.maximum(f, 0) for f in f0]

# ✅ ConvMax도 filters 인자 받도록 수정
def ConvMax(nimg, filters):
    f0 = ConvD(nimg, filters)
    f0 = ReLU(f0)
    fg = Pooling(f0)
    return f0, fg

def draw(f0, fg0, size=(12, 8), k=-1):
    plt.figure(figsize=size)
    for i in range(len(f0)):
        plt.subplot(2, len(f0), i+1)
        plt.title(f'Conv{k}-{i}')
        plt.imshow(f0[i])

    for i in range(len(fg0)):
        plt.subplot(2, len(fg0), len(f0)+i+1)
        plt.title(f'MaxP{k}-{i}')
        plt.imshow(fg0[i])

    if k != -1:
        plt.savefig('conv'+str(k)+'.png')
    plt.show()

def join(mm):
    mm = np.array(mm)
    return np.transpose(mm, (1, 2, 0))  # (채널, 높이, 너비) -> (높이, 너비, 채널)

# ✅ filters 인자 추가
def ConvDraw(p0, filters, size=(12, 8), k=-1):
    f0, fg0 = ConvMax(p0, filters)
    f0 = to_img(f0)
    fg1 = to_img(fg0)
    draw(to_img(f0), to_img(fg0), size, k)
    return join(fg0)

# 테스트 실행
nimg31 = np.random.rand(10, 10)
filters = [np.ones((3,3))] *3

m0 = ConvDraw(nimg31, filters, size=(12, 10), k=0)
```
![CNN_실습](/images/250630_CNN실습_capture.png)
