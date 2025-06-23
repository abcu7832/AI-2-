`timescale 1ns / 1ps

module stopwatch (//top module
    input        clk,
    input        reset,
    input        sw1,
    input        btnR_Clear,
    input        btnL_RunStop,
    output [$clog2(100)-1:0] msec,
    output [$clog2(60)-1:0] sec, 
    output [$clog2(60)-1:0] min,
    output [$clog2(24)-1:0] hour
);
    wire w_clear, w_runstop;

    stopwatch_cu U_StopWatch_CU(
        .clk(clk),
        .reset(reset),
        .i_clear(btnR_Clear&sw1),
        .i_runstop(btnL_RunStop&sw1),
        .o_clear(w_clear),
        .o_runstop(w_runstop)
    );

    stopwatch_dp U_Stopwatch_DP(
        .clk(clk),
        .reset(reset),
        .run_stop(w_runstop),
        .clear(w_clear),
        .msec(msec),
        .sec(sec),
        .min(min),
        .hour(hour)
    );
endmodule