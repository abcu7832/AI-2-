`timescale 1ns / 1ps

module tb_TOP();
    reg clk;
    reg [1:0] motor_direction;
    reg reset;
    reg BTNC;
    reg BTNU;
    reg BTND;
    wire o_run;
    wire [3:0] o_state;
    wire [1:0] in1_in2;
    wire [7:0] fnd_data;
    wire [3:0] fnd_com;

    TOP dut(
        .clk(clk),
        .motor_direction(motor_direction),//sw3, sw2
        .reset(reset),//btnl
        .BTNC(BTNC),
        .BTNU(BTNU),
        .BTND(BTND),
        .o_run(o_run),
        .o_state(o_state),
        .in1_in2(in1_in2),
        .fnd_data(fnd_data),
        .fnd_com(fnd_com)
    );

    always #5 clk = ~clk;

    initial begin
        #0; clk = 0; motor_direction = 0; reset = 1; BTNC = 0; BTNU = 0; BTND = 0;
        #20; reset = 0;
        #1000; BTNC = 1;
        #20000000; BTNC = 0;
        #100; BTNU = 1;
        #20000000; BTNU = 0;
        #100; BTNU = 1;
        #20000000; BTNU = 0;
        #100; BTNU = 1;
        #20000000; BTNU = 0;
        #100; BTND = 1;//RUN
        #20000000; BTND = 0;
        #(3000000*1000); BTND = 1;
        #20000000; BTND = 0;
        #100; BTND = 1;
        #20000000; BTND = 0;
        #(2000000*1000); //IDLE
        $stop;
    end
endmodule
