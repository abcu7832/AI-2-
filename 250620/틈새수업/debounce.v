`timescale 1ns / 1ps

module debounce(
    input clk,
    input i_btn,
    output o_btn
);
    reg [$clog2(1000000):0] count = 0;
    reg clk_10ms = 0, clk_10ms_trig = 0;
    reg o_btn_r = 0;
    
    assign  o_btn = o_btn_r;
    // 100MHz => 10ns * 1000
    // 10ms 주기 
    always @(posedge clk) begin
        if(count == 1000000 - 1) begin
            clk_10ms <= (clk_10ms) ? 1'b0 : 1'b1;
            count <= 0;
        end
        if((clk_10ms_trig == 0)&&(clk_10ms == 1)) begin
            o_btn_r <= i_btn;
        end
        count <= count + 1;
        clk_10ms_trig <= clk_10ms;
    end
endmodule

