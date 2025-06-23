`timescale 1ns / 1ps

module FND_FINISH(
    input clk,
    input reset,
    input state,
    output reg [7:0] fnd_data,
    output reg [3:0] fnd_com,
    output finish
);
    reg [1:0] r_counter;
    reg [$clog2(50000000):0] count = 0;
    reg [2:0] FND_CNT = 0;
    reg r_finish = 0;
    assign finish = r_finish;

    //4진 카운터
    always @(posedge clk, posedge reset) begin
        if (reset) begin
            r_counter <= 0;
        end else begin
            r_counter <= r_counter + 1;
        end
    end
    // 2X4디코더
    always @(r_counter) begin
        case (r_counter)
            2'b00: begin
                fnd_com = 4'b1110;  // fnd 일의 자리 on
            end
            2'b01:   fnd_com = 4'b1101;
            2'b10:   fnd_com = 4'b1011;
            2'b11:   fnd_com = 4'b0111;
            default: fnd_com = 4'b1111;
        endcase
    end
    // fnd_data 관련
    reg state_trig = 0;

    always @(posedge clk, posedge reset) begin
        if (reset) begin
            count <= 0;
        end else begin
            // state 상승에지 감지
            if(~state_trig & state) begin
                count <= 0;
                FND_CNT <= 0;
            end
            state_trig <= state;
            //틱 발생 위함
            if(r_finish) begin
                r_finish <= 1'b0;
            end
            // 0.5s마다 껌뻑껌뻑
            if(count == 50000000 - 1) begin 
                if(FND_CNT == 7) begin
                    r_finish <= 1;
                end
                count <= 0; 
                fnd_data <= (fnd_data == 8'hbf) ? 8'hc0 : 8'hbf;// 8'hfd => ----
                FND_CNT <= FND_CNT + 1;
            end else begin
                count <= count + 1;
            end
        end
    end
endmodule
