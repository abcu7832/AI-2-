`timescale 1ns / 1ps

module CU(
    input            clk,
    input            rst,
    //  G, C, U, D, , 1, 2, 3, M, E
    input      [7:0] rx_data,
    input            rx_done,
    // 틱으로 발생하는 output
    output           go_stop,
    output           clear,
    output           up,
    output           down,
    // 긴 신호로 발생하는 output
    output reg       hour_ctrl,
    output reg       min_ctrl,
    output reg       sec_ctrl,
    output reg       mode,
    output reg       hs_mode
);
    reg tick_reg, tick_next, zero;

    assign go_stop = (rx_data == 8'h47) ? tick_reg : 0; // G
    assign clear = (rx_data == 8'h43) ? tick_reg : 0; // C
    assign up = (rx_data == 8'h55) ? tick_reg : 0; // U
    assign down = (rx_data == 8'h44) ? tick_reg : 0; // D

    always @(posedge clk, posedge rst) begin
        if (rst) begin
            tick_reg <= 0;
            hour_ctrl <= 0;
            min_ctrl <= 0;
            sec_ctrl <= 0;
            mode <= 0;
            hs_mode <= 0;
            zero <= 0;
        end else begin
            tick_reg <= rx_done & tick_next;
            if(rx_done) begin
                case (rx_data)
                    8'h31: hour_ctrl <= (hour_ctrl == 0)? 1: 0; // 1
                    8'h32: min_ctrl <= (min_ctrl == 0)? 1: 0; // 2
                    8'h33: sec_ctrl <= (sec_ctrl == 0)? 1: 0; // 3
                    8'h4d: mode <= (mode == 0)? 1: 0; // M
                    8'h45: hs_mode <= (hs_mode == 0)? 1: 0; // E
                    default: zero <= 0;
                endcase
            end
        end
    end

    always @(*) begin
        tick_next = tick_reg;
        case (rx_data)
            8'h47: tick_next = 1'b1;
            8'h43: tick_next = 1'b1;
            8'h55: tick_next = 1'b1;
            8'h44: tick_next = 1'b1;
            default: tick_next = 1'b0;
        endcase
    end
endmodule
