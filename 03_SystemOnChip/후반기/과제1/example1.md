## RRC Filter(Root Raised Cosine Filter)
### 이론 정리
![filter](/images/250716_6.png)
![filter](/images/250716_4.png)


* 구조 구현은 shift register를 이용하기로 결정!!!
### 코드
```systemverilog
`timescale 1ns / 1ps

module rrc_filter #(
    parameter DATA_WIDTH = 7,
    parameter COEFF_WIDTH = 16,
    parameter TAP_NUM = 33,
    parameter SCALE_SHIFT = 8  // 결과값을 얼마나 줄일지
)(
    input  logic clk,
    input  logic rstn,
    input  logic signed [DATA_WIDTH-1:0] data_in, // <1.6>
    output logic signed [DATA_WIDTH-1:0] data_out  // <1.6>
);

    // 고정 계수 (실제 값으로 교체 필요)
    logic signed [COEFF_WIDTH-1:0] coeffs [0:TAP_NUM-1] = '{
        16'sd0,  -16'sd1,  16'sd1,  16'sd0,  -16'sd1,  16'sd2,  16'sd0,  -16'sd2,
        16'sd2,  16'sd0, -16'sd6, 16'sd8, 16'sd10, -16'sd28, -16'sd14, 16'sd111,
        16'sd196, 16'sd111, -16'sd14, -16'sd28, 16'sd10, 16'sd8, -16'sd6, 16'sd0,
        16'sd2,  -16'sd2,  16'sd0,  16'sd2,  -16'sd1,  16'sd0,  16'sd1,  -16'sd1,
        16'sd0
    };

    // 앞단 입력 레지스터 (D F/F)
    logic signed [DATA_WIDTH-1:0] data_in_reg;

    // 시프트 레지스터
    logic signed [DATA_WIDTH-1:0] shift_reg [0:TAP_NUM-1];

    // 누산기
    logic signed [DATA_WIDTH + COEFF_WIDTH - 1:0] acc;
    logic signed [DATA_WIDTH + COEFF_WIDTH - 1:0] scaled;

    integer i;

    always_ff @(posedge clk or negedge rstn) begin
        if (~rstn) begin
            data_in_reg <= '0;
            for (i = 0; i < TAP_NUM; i++) begin
                shift_reg[i] <= '0;
            end
        end else begin
            data_in_reg <= data_in;  // 앞단 D F/F
            // 시프트 입력 샘플
            for (i = TAP_NUM-1; i > 0; i--) begin
                shift_reg[i] <= shift_reg[i-1];
            end
            shift_reg[0] <= data_in;
        end
    end

    integer j;

    // 뒷단 출력 레지스터 (D F/F)
    logic signed [DATA_WIDTH-1:0] data_out_reg;
    
    assign data_out = data_out_reg;
    
    // FIR 필터 누산 및 스케일링
    always_comb begin
        acc = 0;
        for (j = 0; j < TAP_NUM; j++) begin
            acc += shift_reg[j] * coeffs[j];
        end
        scaled = acc >>> SCALE_SHIFT;
    end

    // 출력 처리 
    always_ff @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            data_out_reg <= '0;
        end else begin
            // 클리핑
            if (scaled > 63)
                data_out_reg <= 7'sd63;
            else if (scaled < -64)
                data_out_reg <= -7'sd64;
            else
                data_out_reg <= {scaled[DATA_WIDTH + COEFF_WIDTH - 1], scaled[5:0]};
        end
    end
endmodule
```
### RRC Filtertestbench 
* data_in: ofdm_i_adc_serial_out_fixed_30dB.txt에 저장된 값
```systemverilog
`timescale 1ns / 1ps

module tb_rrc_filter();

logic clk, rstn;
logic [6:0] data_in;
logic [6:0] data_out;

rrc_filter DUT (
    .clk(clk),
    .rstn(rstn),
    .data_in(data_in), // <1.6>
    .data_out(data_out)  // <1.6>
);

always #5 clk <= ~clk;

integer               data_file    ; // file handler
integer               scan_file    ; // file handler
logic   signed [6:0] captured_data;
int i;
`define NULL 0

initial begin
        clk <= 1'b1;
        rstn <= 1'b0;
        i=0;
        #55 rstn <= 1'b1;
        #789960 $finish;
end

initial begin
        data_file = $fopen("ofdm_i_adc_serial_out_fixed_30dB.txt", "r");
        if (data_file == `NULL) begin
                $display("data_file handle was NULL");
        end
end

always @(posedge clk) begin
        if (!$feof(data_file) && rstn) begin
                scan_file = $fscanf(data_file, "%d\n", captured_data);
                data_in <= captured_data;
        end else begin
                data_in <= 0;
        end
end

integer output_file;

initial begin
    output_file = $fopen("output.txt", "w");
    if (output_file == `NULL) begin
        $display("output_file handle was NULL");
        $finish;
    end
end

always @(posedge clk) begin
        // 파일에 data_out 값을 10진수로 기록
        if(data_out === 'x) begin

        end else begin
                $fwrite(output_file, "%0d\n", $signed(data_out));
                $fflush(output_file);
        end
end

// 시뮬레이션 끝나면 파일 닫기
final begin
        $fwrite(output_file, "-");
        $fflush(output_file);
        $fclose(output_file);
end

endmodule

```
### RRC Filter simulation in matlab
```matlab
clc

%fixed_mode = 0; % '0' = floating
fixed_mode = 1; % '1' = fixed

[FileName, PathName] = uigetfile('*.txt', 'select the capture binary file');
FullPath = fullfile(PathName, FileName);

[FID, message] = fopen(FullPath, 'r');

if (fixed_mode)
    waveform = fscanf(FID, '%d', [1 Inf]);
else
    waveform = fscanf(FID, '%f', [1 Inf]);
end

fclose(FID);

Iwave = waveform(1,:);

figure
pwelch(double(Iwave))
```
![filter_output](/images/250716_1.png)


### 필터가 Low pass filter 역할을 잘해주는 모습
### X축 (정규화 주파수): 신호에 포함된 주파수 성분을 나타냅니다. 0은 직류(DC) 성분, 1은 나이퀴스트 주파수(샘플링 주파수의 절반)에 해당
### Y축 (전력/주파수): 각 주파수 성분이 얼마나 강한 에너지를 갖는지를 데시벨(dB) 단위로 보여줍니다.
----------------------------------
## 이론 정리
* 통과 대역 (Passband): 주파수 0부터 약 0.35까지 비교적 높은 전력 레벨을 유지하는 구간입니다. 이 구간의 주파수 성분들은 필터에 의해 거의 손실 없이 통과했음을 의미. 이게 바로 RRC 필터를 통해 전송하려는 실제 신호가 차지하는 대역폭.
* 천이 대역 (Transition Band): 약 0.35에서 0.4 사이에서 전력이 급격하게 감소하는 구간입니다. 이 기울기는 필터의 롤오프(Roll-off) 특성을 보임. RRC 필터의 '롤오프 팩터(α)' 값에 따라 이 기울기의 완만함이 결정됨.
* 저지 대역 (Stopband): 약 0.4 이후로 전력이 매우 낮은 레벨로 유지되는 구간. 이 구간의 주파수 성분들은 필터에 의해 효과적으로 억제(감쇠)되었음을 의미합니다. 이는 인접 채널에 대한 간섭을 막는 데 매우 중요.
