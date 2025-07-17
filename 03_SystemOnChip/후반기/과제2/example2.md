## RRC Filter(Root Raised Cosine Filter) with pipe register
## 이론 정리
### 구조
* 과제1 example1.md 내용과 동일



![filter](/images/250717_1.png)



=> setup vioation을 방지하기 위해 연산과정에서 pipe register 추가
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
#set per1000  "1000.00";  # ps -> 200 MHz
set per1250 "800.00";

#set dont_care   "2"; 
#set min_delay   "0.3"; 

#set clcon_clk_name "CLK"
set cnt_clk_period "[expr {$per1250*$CLK_MGN}]" 
set cnt_clk_period_h "[expr {$cnt_clk_period/2.0}]"

### I/O DELAY per clock speed
set cnt_clk_delay         [expr "$per1250 * $CLK_MGN * $io_dly"] 

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
### 문제발생
![setuptime_violation](/images/250716_5.png)
### 코드
* module
```systemverilog
`timescale 1ns / 1ps

module fir_filter #(
    parameter DATA_WIDTH = 7,
    parameter COEFF_WIDTH = 16,
    parameter TAP_NUM = 33,
    parameter SCALE_SHIFT = 8
)(
    input  logic clk,
    input  logic rstn,
    input  logic signed [DATA_WIDTH-1:0] data_in,
    output logic signed [DATA_WIDTH- 1:0] data_out
);

    // Shift register (Stage 1)
    logic signed [DATA_WIDTH-1:0] shift_reg [0:32];
    logic signed [DATA_WIDTH-1:0] data_in_reg;
    integer i;

    always_ff @(posedge clk or negedge rstn) begin
        if (!rstn) begin
          	 data_in_reg <= '0;
		 for (i = 0; i < 33; i=i+1) begin 
          		shift_reg[i] <= 0;
          	 end
        end else begin
		data_in_reg <= data_in;
	        for (i = TAP_NUM-1; i > 0; i=i-1) begin 
               		shift_reg[i] <= shift_reg[i-1];
	        end
        	shift_reg[0] <= data_in;
        end
    end
  
    logic signed [DATA_WIDTH + COEFF_WIDTH - 1:0] mult_result [TAP_NUM-1:0];
    integer j;

    // Stage 2: Pipeline register for multiplications
    always_ff @(posedge clk or negedge rstn) begin
	  if(!rstn) begin
		  for(j=0;j<TAP_NUM;j=j+1) begin
			mult_result[j] <= 0;
		  end
	  end else begin
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
    end

    // Stage 3: Sum after multiplication
    logic signed [DATA_WIDTH + COEFF_WIDTH + 6 - 1:0] acc;
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
                data_out_reg <= {scaled[DATA_WIDTH + COEFF_WIDTH - 3], scaled[5:0]};
        end
    end

    assign data_out = data_out_reg;

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
### 합성 결과

### gate simulation

### 필터가 Low pass filter 역할을 잘해주는 모습
### X축 (정규화 주파수): 신호에 포함된 주파수 성분을 나타냅니다. 0은 직류(DC) 성분, 1은 나이퀴스트 주파수(샘플링 주파수의 절반)에 해당
### Y축 (전력/주파수): 각 주파수 성분이 얼마나 강한 에너지를 갖는지를 데시벨(dB) 단위
----------------------------------
## 이론 정리
