## RRC Filter(Root Raised Cosine Filter) with pipe register
### 이론 정리
![filter](/images/250717_1.png)
### 구조
* input: fixed: <1.6>
* coefficient: fixed: <1.8>
* output: fixed: <1.6>
* 구현은 shift register를 이용하기로 결정!!!
* coefficient 값 정리
* 과제1 example1.md 내용과 동일
![coefficient](/images/250716_5.png)
### 문제발생
![setuptime_violation](/images/250716_5.png)
### 코드
```systemverilog

```
### RRC Filtertestbench 
* data_in: ofdm_i_adc_serial_out_fixed_30dB.txt에 저장된 값
```systemverilog

```
### 합성 결과

### gate simulation

### 필터가 Low pass filter 역할을 잘해주는 모습
### X축 (정규화 주파수): 신호에 포함된 주파수 성분을 나타냅니다. 0은 직류(DC) 성분, 1은 나이퀴스트 주파수(샘플링 주파수의 절반)에 해당
### Y축 (전력/주파수): 각 주파수 성분이 얼마나 강한 에너지를 갖는지를 데시벨(dB) 단위
----------------------------------
## 이론 정리
