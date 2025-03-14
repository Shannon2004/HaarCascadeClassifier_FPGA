`timescale 1ns/1ps

module stagetb;

reg clk;
wire stage_condition;

stages uut (.clk(clk), .stage_condition(stage_condition));

initial begin   
    clk = 0;
    stage_condition = 0;
end

always begin
    #5 clk =~ clk;
end

endmodule