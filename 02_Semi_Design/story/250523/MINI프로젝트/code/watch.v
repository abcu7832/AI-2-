`timescale 1ns / 1ps

module watch (
    input clk,
    input reset,
    input btnU,
    input sw1,  //sw1이 0인 경우 시계 모드, 시계모드에서 값 변경하기 위해 input으로 선언
    input sw2,  //초바꾸기
    input sw3,  //분바꾸기
    input sw4,  //시바꾸기
    input btnD,
    output [6:0] msec,
    output [5:0] sec,
    output [5:0] min,
    output [4:0] hour,
    output o_cuckoo
);
    wire [$clog2(100)-1:0] w_msec;
    wire [$clog2(60)-1:0] w_sec, w_min;
    wire [$clog2(24)-1:0] w_hour;
    wire [1:0] w_op, w_mode;
    wire w_tick_sec_up, w_tick_min_up, w_tick_hour_up;
    wire w_tick_sec_down, w_tick_min_down, w_tick_hour_down;

    watch_cu U_WATCH_btnU (
        .clk(clk),
        .reset(reset),
        .button(btnU),
        .sw1 (sw1),
        .sw2 (sw2),
        .sw3 (sw3),
        .sw4 (sw4),
        .tick_sec(w_tick_sec_up),
        .tick_min(w_tick_min_up),
        .tick_hour(w_tick_hour_up)
    );

    watch_cu U_WATCH_btnD (
        .clk(clk),
        .reset(reset),
        .button(btnD),
        .sw1 (sw1),
        .sw2 (sw2),
        .sw3 (sw3),
        .sw4 (sw4),
        .tick_sec(w_tick_sec_down),
        .tick_min(w_tick_min_down),
        .tick_hour(w_tick_hour_down)
    );

    watch_dp U_Watch_DP (
        .clk  (clk),
        .reset(reset),
        .tick_sec_up(w_tick_sec_up),
        .tick_min_up(w_tick_min_up),
        .tick_hour_up(w_tick_hour_up),
        .tick_sec_down(w_tick_sec_down),
        .tick_min_down(w_tick_min_down),
        .tick_hour_down(w_tick_hour_down),
        .msec (msec),
        .sec  (sec),
        .min  (min),
        .hour (hour)
    );

    cuckoo U_Cuckoo (
        .hour(hour),
        .min(min),
        .o_cuckoo(o_cuckoo)
    );
endmodule
