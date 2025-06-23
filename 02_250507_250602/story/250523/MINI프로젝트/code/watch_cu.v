`timescale 1ns / 1ps

module watch_cu(
    input clk,
    input reset,
    input button,
    input sw1,  //sw1이 0인 경우 시계 모드, 시계모드에서 값 변경하기 위해 input으로 선언
    input sw2,  //초바꾸기
    input sw3,  //분바꾸기
    input sw4,  //시바꾸기
    output reg tick_sec,  // watch를 어떻게 컨트롤 할 것인지
    output reg tick_min,
    output reg tick_hour
);
    reg button_prev;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            button_prev <= 0;
            tick_sec <= 0;
            tick_min <= 0;
            tick_hour <= 0;
        end else if((sw1 == 0) && (sw2 == 1)) begin
            button_prev <= button;
            tick_sec <= (~button_prev & button);
        end else if((sw1 == 0) && (sw3 == 1)) begin
            button_prev <= button;
            tick_min <= (~button_prev & button);
        end else if((sw1 == 0) && (sw4 == 1)) begin
            button_prev <= button;
            tick_hour <= (~button_prev & button);
        end else begin
            button_prev <= 0;
            tick_sec <= 0;
            tick_min <= 0;
            tick_hour <= 0;
        end
    end
endmodule