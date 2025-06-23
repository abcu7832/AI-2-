`timescale 1ns / 1ps

module tb_microwave();
    reg clk;
    reg BTNC;
    reg BTNU;
    reg BTND;
    wire [$clog2(60):0] o_sec;

    microwave dut(
        .clk(clk),
        .BTNC(BTNC),
        .BTNU(BTNU),
        .BTND(BTND),
        .o_sec(o_sec)
    );

    always #5 clk = ~clk;

    initial begin
        #0; clk = 0; BTNC = 0; BTNU = 0; BTND = 0;
        #20; BTNC = 1;
        #20; BTNU = 1;
        #20; BTNU = 0;
        #20; BTNU = 1;
        #20; BTNU = 0;
        #20; BTND = 1;
        #20; BTND = 0;
        #100000000;
        $stop;
    end 
endmodule
