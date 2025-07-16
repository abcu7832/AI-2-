/*`timescale 1ns / 1ps

module cuckoo (
    input rst,
    input [4:0] hour,
    input [5:0] min,
    output o_cuckoo
);
    reg r_cuckoo;
    reg [5:0] prev_min, r_min;
    assign o_cuckoo = r_cuckoo;

    always @(*) begin
        r_min = min;
        if (rst) begin
            r_cuckoo = 1'b0;
            prev_min = r_min;
        end else begin
            if ((5'd0 <= hour) && (hour < 5'd7)) begin
                r_cuckoo = 1'b0;
                prev_min = r_min;
            end else begin
                if ((prev_min == 6'd59) && (r_min == 6'd00)) begin
                        r_cuckoo = 1'b1;
                        prev_min = 6'd59;
                end else begin
                    r_cuckoo = 1'b0;
                    prev_min = r_min;
                end
            end
        end
    end
endmodule
*/

`timescale 1ns / 1ps

module cuckoo (
    input  [4:0] hour,
    input  [5:0] min,
    output       o_cuckoo
);
    assign o_cuckoo = (min == 6'd0) & (hour>=7);

endmodule
