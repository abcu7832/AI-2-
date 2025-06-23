`timescale 1ns / 1ps

module microwave(
    input clk,
    input BTNC,
    input BTNU,
    input BTND,
    input finish,
    output [$clog2(1000):0] o_sec, // FND에 연결할 예정
    output reg o_run,
    output [3:0] o_state
);

    parameter IDLE = 0, SETTING = 1, RUN = 2, FINISH = 3;
    reg tick_BTNC = 0, tick_BTNU = 0, tick_BTND = 0;
    reg [$clog2(1000):0] sec = 0;
    reg [$clog2(100000000):0] count = 0;
    reg [1:0] state = 0;

    assign o_state[3] = (state == FINISH) ? 1 : 0;
    assign o_state[2] = (state == RUN) ? 1 : 0;
    assign o_state[1] = (state == SETTING) ? 1 : 0;
    assign o_state[0] = (state == IDLE) ? 1 : 0;
    assign o_sec = sec;

    //FSM
    always @(posedge clk) begin
        case (state) 
            IDLE: begin
                o_run <= 0;
                count <= 0;
                sec <= 0;
                if(tick_BTNC) begin
                    state <= SETTING;
                end
            end
            SETTING: begin
                o_run <= 0;
                if(tick_BTNC) begin
                    state <= IDLE;
                end else if(tick_BTNU) begin
                    sec <= sec + 10;// up button 누르면 10s씩 증가
                end else if(tick_BTND) begin
                    state <= RUN;
                end
            end
            RUN: begin
                o_run <= 1;
                if(tick_BTND) begin
                    state <= SETTING;
                end 
                if(sec == 0) begin
                    //state <= IDLE;
                    state <= FINISH;
                    count <= 0;
                end
                if(count == 100000000 - 1) begin
                    count <= 0;
                    sec <= sec - 1; 
                end else begin
                    count <= count + 1;    
                end
            end
            FINISH: begin
                if(finish) begin
                   state <= IDLE; 
                end
            end
        endcase
    end

    reg BTNC_trig = 0, BTNU_trig = 0, BTND_trig = 0;

    // button tick gen
    always @(posedge clk) begin
        if((BTNC_trig == 0)&&(BTNC == 1)) begin
            tick_BTNC <= 1;
        end else begin
            tick_BTNC <= 0;
        end
        if((BTNU_trig == 0)&&(BTNU == 1)) begin
            tick_BTNU <= 1;
        end else begin
            tick_BTNU <= 0;
        end
        if((BTND_trig == 0)&&(BTND == 1)) begin
            tick_BTND <= 1;
        end else begin
            tick_BTND <= 0;
        end
        BTNC_trig <= BTNC;
        BTNU_trig <= BTNU;
        BTND_trig <= BTND;
    end
endmodule
