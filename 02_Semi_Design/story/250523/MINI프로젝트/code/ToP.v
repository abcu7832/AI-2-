`timescale 1ns / 1ps

module ToP(
    input        clk,
    input        reset,
    input        rx,
    input        btnU,
    input        btnL_RunStop,
    input        btnR_Clear,
    input        btnD,
    input        sw0,
    input        sw1,
    input        sw2,
    input        sw3,
    input        sw4,
    output       tx,
    output [3:0] LED,
    output [7:0] fnd_data,
    output [3:0] fnd_com,
    output       o_cuckoo
);

    wire [7:0] w_rx_data;
    wire rx_done, tx_done;
    wire w_go_stop, w_clear, w_up, w_down, w_hour_ctrl, w_min_ctrl, w_sec_ctrl;
    wire w_mode, w_hs_mode;

    uart_controller U_Uart_CTRL(
        .clk(clk),
        .rst(reset),
        .btn_start(btnU),
        .rx(rx),
        .rx_data(w_rx_data),
        .rx_done(rx_done),
        .tx_done(tx_done),
        .tx(tx)
    );

    CU U_CU(
        .clk(clk),
        .rst(reset),
        .rx_data(w_rx_data),
        .rx_done(rx_done),
        .go_stop(w_go_stop),
        .clear(w_clear),
        .up(w_up),
        .down(w_down),
        .hour_ctrl(w_hour_ctrl),
        .min_ctrl(w_min_ctrl),
        .sec_ctrl(w_sec_ctrl),
        .mode(w_mode),
        .hs_mode(w_hs_mode)
    );

    TOP_WATCH U_TOP_WATCH(
        .clk(clk),
        .reset(reset),
        .btnU(btnU),
        .btnL_RunStop(btnL_RunStop),
        .btnR_Clear(btnR_Clear),
        .btnD(btnD),
        .u_go_stop(w_go_stop),
        .u_clear(w_clear),
        .u_up(w_up),
        .u_down(w_down),
        .sw0(sw0 | w_hs_mode),
        .sw1(sw1 | w_mode),
        .sw2(sw2 | w_sec_ctrl),
        .sw3(sw3 | w_min_ctrl),
        .sw4(sw4 | w_hour_ctrl),
        .LED(LED),
        .fnd_data(fnd_data),
        .fnd_com(fnd_com),
        .o_cuckoo(o_cuckoo)
    );
endmodule
