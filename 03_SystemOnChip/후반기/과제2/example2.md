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
`timescale 1ns / 1ps

module fir_filter #(
    parameter DATA_WIDTH = 7,
    parameter COEFF_WIDTH = 9,
    parameter TAP_NUM = 33,
    parameter SCALE_SHIFT = 8
)(
    input  logic clk,
    input  logic rstn,
    input  logic signed [DATA_WIDTH-1:0] data_in,
    output logic signed [DATA_WIDTH + COEFF_WIDTH + 6 - 1:0] acc
);

    // Shift register (Stage 1)
    logic signed [DATA_WIDTH-1:0] shift_reg [32:0];
    integer i;

    always_ff @(posedge clk or negedge rstn) begin
        if (!rstn) begin
          	 for (i = TAP_NUM-1; i > 0; i=i-1) begin 
          			shift_reg[i] <= 0;
          	 end
        end 
        else begin
            for (i = TAP_NUM-1; i > 0; i=i-1) begin 
               shift_reg[i] <= shift_reg[i-1];
            end
            shift_reg[0] <= data_in;
        end
    end
  
    logic signed [DATA_WIDTH + COEFF_WIDTH - 1:0] mult_result [TAP_NUM-1:0];
    integer j;

    // Stage 2: Pipeline register for multiplications
    always_ff @(posedge clk) begin
          mult_result[0] <= shift_reg[0] * 0;
          mult_result[1] <= shift_reg[1] * (-1);
          mult_result[2] <= shift_reg[2] * (1);
          mult_result[3] <= shift_reg[3] * 0;
          mult_result[4] <= shift_reg[4] * (-1);
          mult_result[5] <= shift_reg[5] * 2;
          mult_result[6] <= shift_reg[6] * 0;
          mult_result[7] <= shift_reg[7] * (-2);
          mult_result[8] <= shift_reg[8] * 2;
          mult_result[9] <= shift_reg[9] * 0;
          mult_result[10] <= shift_reg[10] * (-6);
          mult_result[11] <= shift_reg[11] * 8;
          mult_result[12] <= shift_reg[12] * 10;
          mult_result[13] <= shift_reg[13] * (-28);
          mult_result[14] <= shift_reg[14] * (-14);
          mult_result[15] <= shift_reg[15] * 111;
          mult_result[16] <= shift_reg[16] * 196;
          mult_result[17] <= shift_reg[17] * 111;
          mult_result[18] <= shift_reg[18] * (-14);
          mult_result[19] <= shift_reg[19] * (-28);
          mult_result[20] <= shift_reg[20] * 10;
          mult_result[21] <= shift_reg[21] * 8;
          mult_result[22] <= shift_reg[22] * (-6);
          mult_result[23] <= shift_reg[23] * 0;
          mult_result[24] <= shift_reg[24] * 2;
          mult_result[25] <= shift_reg[25] * (-2);
          mult_result[26] <= shift_reg[26] * 0;
          mult_result[27] <= shift_reg[27] * 2;
          mult_result[28] <= shift_reg[28] * (-1);
          mult_result[29] <= shift_reg[29] * 0;
          mult_result[30] <= shift_reg[30] * (1);
          mult_result[31] <= shift_reg[31] * (-1);
          mult_result[32] <= shift_reg[32] * 0;
    end

    // Stage 3: Sum after multiplication
    logic signed [DATA_WIDTH + COEFF_WIDTH - 3:0] scaled;
    integer k;

    always_comb begin
        acc = mult_result[0] + mult_result[1] + mult_result[2] + mult_result[3] + mult_result[4] + mult_result[5] + mult_result[6] + mult_result[7] + mult_result[8] + mult_result[9] + mult_result[10] + mult_result[11] + mult_result[12] + mult_result[13] + mult_result[14] + mult_result[15] + mult_result[16] + mult_result[17] + mult_result[18] + mult_result[19] + mult_result[20] + mult_result[21] + mult_result[22] + mult_result[23] + mult_result[24] + mult_result[25] + mult_result[26] + mult_result[27] + mult_result[28] + mult_result[29] + mult_result[30] + mult_result[31] + mult_result[32]; 
	      scaled = acc >>> SCALE_SHIFT;
    end

    // Output register with clipping
    logic signed [DATA_WIDTH-1:0] data_out_reg;
    always_ff @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            data_out_reg <= '0;
        end else begin
            if (scaled > 63)
                data_out_reg <= 7'sd63;
            else if (scaled < -64)
                data_out_reg <= -7'sd64;
            else
                data_out_reg <= {scaled[DATA_WIDTH + COEFF_WIDTH - 1], scaled[5:0]};
        end
    end

    assign data_out = data_out_reg;

endmodule
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
