`timescale 1ns / 1ps

module TOP(
    input clk,
    input [1:0] motor_direction,//sw3, sw2
    input reset,//btnl
    input BTNC,
    input BTNU,
    input BTND,
    output o_run,
    output [3:0] o_state,
    output [1:0] in1_in2,
    output [7:0] fnd_data,
    output [3:0] fnd_com
);
    wire w_BTNC, w_BTNU, w_BTND;
    wire [$clog2(1000):0] w_sec;

    assign in1_in2 = motor_direction;

    debounce U_BTNC_DEBOUNCE (
        .clk(clk),
        .i_btn(BTNC),
        .o_btn(w_BTNC)
    );

    debounce U_BTNU_DEBOUNCE (
        .clk(clk),
        .i_btn(BTNU),
        .o_btn(w_BTNU)
    );

    debounce U_BTND_DEBOUNCE (
        .clk(clk),
        .i_btn(BTND),
        .o_btn(w_BTND)
    );
    wire finish;

    microwave U_MICROWAVE(
        .clk(clk),
        .BTNC(w_BTNC),
        .BTNU(w_BTNU),
        .BTND(w_BTND),
        .finish(finish),
        .o_sec(w_sec), // FND에 연결할 예정
        .o_run(o_run),
        .o_state(o_state)
    );

    wire [7:0] g_fnd_data, f_fnd_data;
    wire [3:0] g_fnd_com, f_fnd_com;

    FND_CTRL U_FND (
        .clk(clk),
        .reset(reset),
        .count_data(w_sec),
        .fnd_data(g_fnd_data),
        .fnd_com(g_fnd_com)
    );

    FND_FINISH U_FND_FINISH (
        .clk(clk),
        .reset(reset),
        .state(o_state[3]),
        .fnd_data(f_fnd_data),
        .fnd_com(f_fnd_com),
        .finish(finish)
    );

    FND_CU U_FND_CTRL (
        .state(o_state[3]),
        .g_FND_DATA(g_fnd_data),
        .g_FND_COM(g_fnd_com),
        .f_FND_DATA(f_fnd_data),
        .f_FND_COM(f_fnd_com),
        .FND_DATA(fnd_data),
        .FND_COM(fnd_com)
    );
endmodule

module FND_CU(
    input state,
    input [7:0] g_FND_DATA,
    input [3:0] g_FND_COM,
    input [7:0] f_FND_DATA,
    input [3:0] f_FND_COM,
    output [7:0] FND_DATA,
    output [3:0] FND_COM
);
    assign FND_DATA = (state)?f_FND_DATA:g_FND_DATA;
    assign FND_COM = (state)?f_FND_COM:g_FND_COM;
endmodule
