## RRC Filter(Root Raised Cosine Filter)
### 이론 정리
![filter](/images/250716_6.png)
![filter](/images/250716_4.png)


* 구조 구현은 shift register를 이용하기로 결정!!!
```systemverilog
`timescale 1ns / 1ps

module fir_filter #(
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

fir_filter DUT (
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
### RRC Filter simulation
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
