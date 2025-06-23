`timescale 1ns / 1ps

module TOP_WATCH (
    input        clk,
    input        btnU,
    input        btnL_RunStop,
    input        btnR_Clear,
    input        btnD,
    input        u_go_stop,
    input        u_clear,
    input        u_up,
    input        u_down,
    input        reset,
    input        sw0,
    input        sw1,
    input        sw2,
    input        sw3,
    input        sw4,
    output [3:0] LED,
    output [7:0] fnd_data,
    output [3:0] fnd_com,
    output       o_cuckoo
);
    // sw[0] 시,분/ 초,ms 모드
    // sw[1] 시계모드, 스톱워치 모드
    wire [6:0] s_msec, w_msec, f_msec;
    wire [5:0] s_sec, w_sec, f_sec;
    wire [5:0] s_min, w_min, f_min;
    wire [4:0] s_hour, w_hour, f_hour;
    wire w_btnR, w_btnL, w_btnU, w_btnD;

    assign f_msec = (sw1 == 0) ? w_msec : s_msec;
    assign f_sec  = (sw1 == 0) ? w_sec : s_sec;
    assign f_min  = (sw1 == 0) ? w_min : s_min;
    assign f_hour = (sw1 == 0) ? w_hour : s_hour;

    assign LED[0] = (~sw1 & ~sw0);
    assign LED[1] = (~sw1 & sw0);
    assign LED[2] = (sw1 & ~sw0);
    assign LED[3] = (sw1 & sw0);

    btn_device U_btnR (
        .clk  (clk),
        .rst  (reset),
        .i_btn(btnR_Clear),
        .o_btn(w_btnR)
    );

    btn_device U_btnL (
        .clk  (clk),
        .rst  (reset),
        .i_btn(btnL_RunStop),
        .o_btn(w_btnL)
    );

    btn_device U_btnU (
        .clk  (clk),
        .rst  (reset),
        .i_btn(btnU),
        .o_btn(w_btnU)
    );

    btn_device U_btnD (
        .clk  (clk),
        .rst  (reset),
        .i_btn(btnD),
        .o_btn(w_btnD)
    );

    stopwatch U_STOPWATCH (
        .clk(clk),
        .reset(reset),
        .sw1(sw1),
        .btnR_Clear(w_btnR | u_clear),
        .btnL_RunStop(w_btnL | u_go_stop),
        .msec(s_msec),
        .sec(s_sec),
        .min(s_min),
        .hour(s_hour)
    );

    watch U_Watch (
        .clk(clk),
        .reset(reset),
        .btnU(w_btnU | u_up),
        .sw1(sw1),//sw1이 0인 경우 시계 모드, 시계모드에서 값 변경하기 위해 input으로 선언
        .sw2(sw2),  //초바꾸기
        .sw3(sw3),  //분바꾸기
        .sw4(sw4),  //시바꾸기
        .btnD(w_btnD | u_down),
        .msec(w_msec),
        .sec(w_sec),
        .min(w_min),
        .hour(w_hour),
        .o_cuckoo(o_cuckoo)
    );

    fnd_controller U_FND_CONTROLLER (
        .clk(clk),
        .rst(reset),
        .sw0(sw0),
        .msec(f_msec),
        .sec(f_sec),
        .min(f_min),
        .hour(f_hour),
        .fnd_data(fnd_data),
        .fnd_com(fnd_com)
    );
endmodule

