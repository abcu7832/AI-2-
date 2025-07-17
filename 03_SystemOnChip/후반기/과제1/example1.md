## RRC Filter(Root Raised Cosine Filter)
### 이론 정리
![filter](/images/250716_6.png)
![filter](/images/250716_4.png)
### 구조
* input: fixed: <1.6>
* coefficient: fixed: <1.8>
* output: fixed: <1.6>
* 구현은 shift register를 이용하기로 결정!!!
* coefficient 값 정리
![coefficient](/images/250716_5.png)
### 환경
* sdc파일
```bash
#-----------------------------------------------------------------------
#  case &  clock definition 
#-----------------------------------------------------------------------
## FF to FF clock period margin
set CLK_MGN  0.7  
## REGIN, REGOUT setup/hold margin
#set io_dly   0.15 
set io_dly   0.05 


#set per200  "5.00";  # ns -> 200 MHz
set per1000  "1000.00";  # ps -> 200 MHz
#set per1250 "800.00";

#set dont_care   "2"; 
#set min_delay   "0.3"; 

#set clcon_clk_name "CLK"
set cnt_clk_period "[expr {$per1000*$CLK_MGN}]" 
set cnt_clk_period_h "[expr {$cnt_clk_period/2.0}]"

### I/O DELAY per clock speed
set cnt_clk_delay         [expr "$per1000 * $CLK_MGN * $io_dly"] 

#-----------------------------------------------------------------------
#  Create  Clock(s)
#-----------------------------------------------------------------------
#create_clock -name clcon_clk     -period [expr "$per875 * $CLK_MGN"] [get_ports {$clcon_clk_name}]
#create_clock -name clcon_clk     -period $clcon_clk_period -waveform "0 $clcon_clk_period_h" [get_ports {$clcon_clk_name}]
create_clock -name cnt_clk       -period $cnt_clk_period   -waveform "0 $cnt_clk_period_h" [get_ports clk]

#LANE 1 RX CLOCK
#create_generated_clock  -name GC_rxck1_org       -source [get_ports I_A_L1_RX_CLKP ] -divide_by 1 [get_pins u_L1_Rswap/U_CM2X1_nand/ZN]
#create_generated_clock  -name GC_rxck1_swp  -add -source [get_ports I_A_L0_RX_CLKP ] -divide_by 1 [get_pins u_L1_Rswap/U_CM2X1_nand/ZN]


#set_clock_uncertainty -setup 0.05 [all_clocks]
set_clock_uncertainty -setup 50 [all_clocks] 
#set_clock_uncertainty -hold  0.05 [all_clocks]
set_clock_uncertainty -hold  50 [all_clocks]

# -------------------------------------
#set_driving_cell -no_design_rule -lib_cell BUFFD1BWP35P140 -pin Z  [all_inputs] 

set_load            0.2 [all_outputs]
set_max_transition  0.3 [current_design]
set_max_transition  0.15 -clock_path [all_clocks]
set_max_fanout 64       [current_design]

#-----------------------------------------------------------------------
# IO delay define
#-----------------------------------------------------------------------
#(SKW_I2C  )  --> Provide FF list. WILL BE DONE at PINES
#(SKW_REG  )  --> Provide FF list. WILL BE DONE at PINES
#(RXPR,TXPR)  --> Provide FF list. WILL BE DONE at PINES
# -0.7ns is the clock network delay(clk skew). Delay from clock start to FF clk input.
#set_output_delay   -0.7    -clock cnt_clk  [get_ports clk]
#set_output_delay   -700    -clock cnt_clk  [get_ports clk]
#set_output_delay   700    -clock cnt_clk  [get_ports clk]

#(RXDIN  )  -- Setup/Hold
#set_input_delay     0.5    -clock cnt_clk  [get_ports clk]
set_input_delay     500    -clock cnt_clk  [get_ports clk]

#-----------------------------------------------------------
# DONT TOUCH LIST
#-----------------------------------------------------------
##set_dont_touch [ get_designs BUFFD*  ]
##set_dont_touch [ get_designs CKLNQ*  ]
##set_dont_touch [ get_designs U_DLY* ]
#set_dont_touch U_*
#set_dont_touch I2c_reg_MISC*/U_i2cregclk
#set_dont_touch reg_hostreg/U_i2cregclk
#set_dont_touch reg_onedtop/U_i2cregclk
#set_dont_touch dtop_l*/i2c_reg_*/U_i2cregclk
#set_dont_touch dtop_l*/prcon_caltop/i2c_reg_prc_cal/U_i2cregclk

#set_dont_use [get_lib_cells */TIE*]
```
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
### Y축 (전력/주파수): 각 주파수 성분이 얼마나 강한 에너지를 갖는지를 데시벨(dB) 단위
----------------------------------
## 이론 정리
* 통과 대역 (Passband): 주파수 0부터 약 0.35까지 비교적 높은 전력 레벨을 유지하는 구간입니다. 이 구간의 주파수 성분들은 필터에 의해 거의 손실 없이 통과했음을 의미. 이게 바로 RRC 필터를 통해 전송하려는 실제 신호가 차지하는 대역폭.
* 천이 대역 (Transition Band): 약 0.35에서 0.4 사이에서 전력이 급격하게 감소하는 구간입니다. 이 기울기는 필터의 롤오프(Roll-off) 특성을 보임. RRC 필터의 '롤오프 팩터(α)' 값에 따라 이 기울기의 완만함이 결정됨.
* 저지 대역 (Stopband): 약 0.4 이후로 전력이 매우 낮은 레벨로 유지되는 구간. 이 구간의 주파수 성분들은 필터에 의해 효과적으로 억제(감쇠)되었음을 의미합니다. 이는 인접 채널에 대한 간섭을 막는 데 매우 중요.
----------------------------------
* 그렇다면 이 결과가 디지털 통신에서 왜 중요할까? 

대역폭 제한 (Bandwidth Limiting): RRC 필터는 디지털 신호를 특정 주파수 대역 내에 가두는 펄스 성형(Pulse Shaping) 역할을 합니다. 이 시뮬레이션 결과는 필터가 신호의 대역폭을 성공적으로 제한하여, 한정된 주파수 자원을 효율적으로 사용하고 다른 통신 채널에 간섭을 주지 않도록 하고 있음을 보여줍니다.

부호 간 간섭(ISI) 최소화: RRC 필터의 가장 중요한 특징은 이름에 있는 'Root'에 있습니다. 통신 시스템에서는 보통 송신단과 수신단에 각각 RRC 필터를 하나씩 사용합니다. 이 두 개의 RRC 필터가 합쳐지면 **'Raised Cosine 필터'**가 되는데, 이 필터는 수신된 신호에서 부호 간 간섭(Intersymbol Interference, ISI)을 이론적으로 '0'으로 만들 수 있는 특성을 가집니다. ISI가 없어야 '0'과 '1'의 데이터를 정확하게 구분할 수 있습니다.

요약하자면, 이 그래프는 구현하신 RRC 필터가 대역폭을 성공적으로 제한하는 저역 통과 필터의 역할을 잘 수행하고 있음을 시각적으로 확인시켜 주는 중요한 결과입니다. 이는 효율적이고 신뢰도 높은 디지털 통신 시스템을 구현하는 데 있어 핵심적인 부분입니다.
