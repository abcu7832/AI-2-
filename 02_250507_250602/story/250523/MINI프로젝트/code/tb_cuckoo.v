`timescale 1ns / 1ps

module tb_cuckoo();
    reg [4:0] hour;
    reg [5:0] min;
    wire o_cuckoo;

    cuckoo U_cuckoo(
        .hour(hour),
        .min(min),
        .o_cuckoo(o_cuckoo)
    );

    initial begin
        #0; min = 59; hour = 7;
        #100; min = 0; hour = 8;
        #100; min = 1;
        #1000;
        $finish;
    end
endmodule
