`timescale 1ns / 1ps

module tb_CU();
    reg        clk;
    reg        rst;
    reg  [7:0] rx_data;
    reg        rx_done;
    // 틱으로 발생하는 output
    wire       go_stop;
    wire       clear;
    wire       up;
    wire       down;
    // 긴 신호로 발생하는 output
    wire       hour_ctrl;
    wire       min_ctrl;
    wire       sec_ctrl;
    wire       mode;
    wire       hs_mode;

    CU U_cu(
        .clk(clk),
        .rst(rst),
        .rx_data(rx_data),
        .rx_done(rx_done),
        // 틱으로 발생하는 output
        .go_stop(go_stop),
        .clear(clear),
        .up(up),
        .down(down),
        // 긴 신호로 발생하는 output
        .hour_ctrl(hour_ctrl),
        .min_ctrl(min_ctrl),
        .sec_ctrl(sec_ctrl),
        .mode(mode),
        .hs_mode(hs_mode)
    );
    always #5 clk = ~clk;

    initial begin
        #0; clk = 0; rst = 1; rx_data = "M"; rx_done = 0;
        #20; rst = 0; 
        #10; rx_done = 1;
        #10; rx_done = 0;
        #100; rx_data = "0";
        #1000000000;
    end
endmodule
