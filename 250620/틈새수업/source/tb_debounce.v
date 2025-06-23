`timescale 1ns / 1ps

module tb_debounce();
    reg clk;
    reg i_btn;
    wire o_btn;

debounce DUT (
    .clk(clk),
    .i_btn(i_btn),
    .o_btn(o_btn)
);

always #5 clk = ~clk;

initial begin
    #0 clk = 0;  i_btn = 0;
    #20 i_btn = 1;
    #50000000; i_btn = 0;
    #1000000000;
    $stop;
end
endmodule
