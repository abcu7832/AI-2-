`timescale 1ns / 1ps

module watch_dp(
    input        clk,
    input        reset,
    input        tick_sec_up,
    input        tick_min_up,
    input        tick_hour_up,
    input        tick_sec_down,
    input        tick_min_down,
    input        tick_hour_down,
    output [6:0] msec,
    output [5:0] sec,
    output [5:0] min,
    output [4:0] hour
);
    wire w_tick_100hz, w_msec_tick, w_sec_tick, w_min_tick, w_hour_tick;

    tick_gen_watch U_tick_gen_10ms_watch( // 10ms 생성
        .clk(clk),
        .reset(reset),
        .o_tick(w_msec_tick)
    );

    time_counter_10ms_watch #(.TICK_COUNT(100)) U_MSEC_watch (
        .clk(clk),
        .rst(reset),
        .i_tick(w_msec_tick),
        .o_time(msec),
        .o_tick(w_sec_tick)
    );

    time_counter_watch #(.TICK_COUNT(60)) U_SEC_watch (
        .clk(clk),
        .rst(reset),
        .i_tick(w_sec_tick | tick_sec_up),
        .i_down_tick(tick_sec_down),
        .o_time(sec),
        .o_tick(w_min_tick)
    );

    time_counter_watch #(.TICK_COUNT(60)) U_MIN_watch (
        .clk(clk),
        .rst(reset),
        .i_tick(w_min_tick | tick_min_up),
        .i_down_tick(tick_min_down),
        .o_time(min),
        .o_tick(w_hour_tick)
    );

    time_counter_hour_watch #(.TICK_COUNT(24)) U_HOUR_watch (
        .clk(clk),
        .rst(reset),
        .i_tick(w_hour_tick | tick_hour_up),
        .i_down_tick(tick_hour_down),
        .o_time(hour),
        .o_tick()
    );
endmodule

// 10ms 생성 => FCOUNT = 1_000_000
module tick_gen_watch #(parameter FCOUNT = 1_000_000)( // 10ms 생성
    input  clk,
    input  reset,
    output o_tick
);
    reg r_o_tick;
    reg [$clog2(FCOUNT)-1:0] r_counter;

    assign o_tick = r_o_tick;

    always @(posedge clk, posedge reset) begin
        if(reset) begin
            r_counter <= 0;
            r_o_tick <= 0;
        end else begin   
            if(r_counter == FCOUNT - 1) begin
                r_counter <= 0;
                r_o_tick <= 1;
            end else begin
                r_counter <= r_counter + 1;
                r_o_tick <= 0;
            end      
        end
    end
endmodule

// 카운트 후 값 전달
module time_counter_10ms_watch #(
    parameter TICK_COUNT = 100
) (
    input                               clk,
    input                               rst,
    input                               i_tick,
    output     [$clog2(TICK_COUNT)-1:0] o_time,
    output                              o_tick
);

    reg [$clog2(TICK_COUNT)-1:0] count_reg, count_next;
    reg o_tick_reg, o_tick_next;

    assign o_time = count_reg;
    assign o_tick = o_tick_reg;
    
    // state register
    always @(posedge clk, posedge rst) begin
        if(rst) begin
            count_reg <= 0;// nonblock => f/f 사용할때 일반적으로 
            o_tick_reg <= 1'b0;
        end else begin
            count_reg <= count_next; 
            o_tick_reg <= o_tick_next;
        end
    end

    // next state
    always @(*) begin // Combinational logic으로 구현
        count_next = count_reg; 
        o_tick_next = 1'b0;
        if(i_tick == 1'b1) begin
            if (count_reg == (TICK_COUNT - 1)) begin
                count_next = 1'b0;
                o_tick_next = 1'b1;
            end else begin
               count_next = count_reg + 1; 
               o_tick_next = 1'b0;
            end
        end
    end
endmodule

module time_counter_watch #(//초,분
    parameter TICK_COUNT = 100
) (
    input                           clk,
    input                           rst,
    input                           i_tick,
    input                           i_down_tick,
    output [$clog2(TICK_COUNT)-1:0] o_time,
    output                          o_tick
);

    reg [$clog2(TICK_COUNT)-1:0] count_reg, count_next;
    reg o_tick_reg, o_tick_next;

    assign o_time = count_reg;
    assign o_tick = o_tick_reg;
    
    // state register
    always @(posedge clk, posedge rst) begin
        if(rst) begin
            count_reg <= 0;// nonblock => f/f 사용할때 일반적으로 
            o_tick_reg <= 1'b0;
        end else begin
            count_reg <= count_next; 
            o_tick_reg <= o_tick_next;
        end
    end

    // next state
    always @(*) begin // Combinational logic으로 구현
        count_next = count_reg; 
        o_tick_next = 1'b0;
    
        if(i_tick == 1'b1) begin
            if (count_reg == (TICK_COUNT - 1)) begin
                count_next = 0;
                o_tick_next = 1'b1;
            end else begin
               count_next = count_reg + 1; 
               o_tick_next = 1'b0;
            end
        end 
        if(i_down_tick == 1'b1) begin
            count_next = (count_reg == 0) ? 59 : count_reg - 1;
        end
    end
endmodule

// 카운트 후 값 전달
module time_counter_hour_watch #(//시
    parameter TICK_COUNT = 100
) (
    input                           clk,
    input                           rst,
    input                           i_tick,
    input                           i_down_tick,
    output [$clog2(TICK_COUNT)-1:0] o_time,
    output                          o_tick
);

    reg [$clog2(TICK_COUNT)-1:0] count_reg, count_next;
    reg o_tick_reg, o_tick_next;

    assign o_time = count_reg;
    assign o_tick = o_tick_reg;
    
    // state register
    always @(posedge clk, posedge rst) begin
        if(rst) begin
            count_reg <= 12;// nonblock => f/f 사용할때 일반적으로 
            o_tick_reg <= 1'b0;
        end else begin
            count_reg <= count_next; 
            o_tick_reg <= o_tick_next;
        end
    end

    // next state
    always @(*) begin // Combinational logic으로 구현
        count_next = count_reg; 
        o_tick_next = 1'b0;
        if(i_tick == 1'b1) begin
            if (count_reg == (TICK_COUNT - 1)) begin
                count_next = 0;
                o_tick_next = 1'b1;
            end else begin
               count_next = count_reg + 1; 
               o_tick_next = 1'b0;
            end
        end 
        if(i_down_tick == 1'b1) begin
            count_next = (count_reg == 0) ? 23 : count_reg - 1;
        end
    end
endmodule
