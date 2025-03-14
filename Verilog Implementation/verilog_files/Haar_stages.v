module Haar_stages(
    input clk,
    input reset,
	input [15:0] address1,
	input [15:0] no_of_features,
	output stage_condition 
);


reg count1 = 0;

reg [15:0] A1 ;
reg [15:0] B1 ;
reg [15:0] C1 ;
reg [15:0] D1;
reg [15:0] weight1;
reg [15:0] A2 ;
reg [15:0] B2 ;
reg [15:0] C2 ;
reg [15:0] D2 ;
reg [15:0] weight2;
reg [15:0] A3 ;
reg [15:0] B3 ;
reg [15:0] C3 ;
reg [15:0] D3 ;
reg [15:0] weight3 ;

reg [15:0] feature_threshold;
reg [15:0] left_node ;
reg [15:0] right_node;

wire [15:0] out;
wire fvalue_valid;

reg [2:0 ]count;


reg op_done;
reg [1:0] state;
//reg [15:0] no_of_features;
//reg [15:0] address1;
reg [15:0] address;

wire [79:0] rect1;
wire [79:0] rect2;
wire [79:0] rect3;

wire [47:0] wc_info;


reg [15:0] stage_sum = 0;
reg [15:0] final_stage_value = 0;

reg [15:0] stage_threshold;
reg stage_decision;
// reg stage_condition;

wire final_stage_sign;
assign final_stage_sign = final_stage_value[15];


ila_0 your_instance_name (
	.clk(clk), // input wire clk


	.probe0(out), // input wire [15:0]  probe0  
	.probe1(stage_sum), // input wire [15:0]  probe1 
	.probe2(fvalue_valid), // input wire [0:0]  probe2 
	.probe3(op_done), // input wire [0:0]  probe3 
	.probe4(address), // input wire [1:0]  probe4 
	.probe5(stage_decision) // input wire [0:0]  probe5
);



ila_1 ILA1 (
	.clk(clk), // input wire clk


	.probe0(A1), // input wire [29:0]  probe0  
	.probe1(B1), // input wire [29:0]  probe1 
	.probe2(C1), // input wire [29:0]  probe2 
	.probe3(D1), // input wire [29:0]  probe3 
	.probe4(weight1), // input wire [29:0]  probe4 
	.probe5(A2), // input wire [29:0]  probe5 
	.probe6(B2), // input wire [29:0]  probe6 
	.probe7(C2), // input wire [29:0]  probe7 
	.probe8(D2), // input wire [29:0]  probe8 
	.probe9(weight2), // input wire [29:0]  probe9 
	.probe10(A3), // input wire [29:0]  probe10 
	.probe11(B3), // input wire [29:0]  probe11 
	.probe12(C3), // input wire [29:0]  probe12 
	.probe13(D3), // input wire [29:0]  probe13 
	.probe14(out), // input wire [29:0]  probe14 
	.probe15(feature_threshold), // input wire [10:0]  probe15 
	.probe16(left_node), // input wire [10:0]  probe16 
	.probe17(right_node), // input wire [10:0]  probe17 
	.probe18(weight3) // input wire [10:0]  probe18
);



blk_mem_gen_0 rect1_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),      // input wire ena
  .wea(0),      // input wire [0 : 0] wea
  .addra(address),  // input wire [1 : 0] addra
  .dina(0),    // input wire [79 : 0] dina
  .douta(rect1)  // output wire [79 : 0] douta
);


blk_mem_gen_1 rect2_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),      // input wire ena
  .wea(0),      // input wire [0 : 0] wea
  .addra(address),  // input wire [1 : 0] addra
  .dina(0),    // input wire [79 : 0] dina
  .douta(rect2)  // output wire [79 : 0] douta
);

blk_mem_gen_2 rect3_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),      // input wire ena
  .wea(0),      // input wire [0 : 0] wea
  .addra(address),  // input wire [1 : 0] addra
  .dina(0),    // input wire [79 : 0] dina
  .douta(rect3)  // output wire [79 : 0] douta
);

blk_mem_gen_3 wc_info_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),      // input wire ena
  .wea(0),      // input wire [0 : 0] wea
  .addra(address),  // input wire [1 : 0] addra
  .dina(0),    // input wire [47 : 0] dina
  .douta(wc_info)  // output wire [47 : 0] douta
);




initial 
begin
    
op_done = 0;
state = 2'b00;
address = 0;
stage_sum = 0;
stage_threshold = 16'b1111111111110001;
count = 0;

end

// always @(posedge clk) begin
// 	 address = address1;
// end


WeakClassifier w1(clk,op_done,A1,B1,C1,D1,weight1,A2,B2,C2,D2,weight2,A3,B3,C3,D3,weight3,feature_threshold,left_node,right_node,out,fvalue_valid);



always @(posedge clk)
begin

    A1 <= rect1[79:64];
    B1 <= rect1[63:48];
    C1 <= rect1[47:32];
    D1 <= rect1[31:16];
    weight1 <= rect1[15:0];


    A2 <= rect2[79:64];
    B2 <= rect2[63:48];
    C2 <= rect2[47:32];
    D2 <= rect2[31:16];
    weight2 <= rect2[15:0];


    A3 <= rect3[79:64];
    B3 <= rect3[63:48];
    C3 <= rect3[47:32];
    D3 <= rect3[31:16];
    weight3 <= rect3[15:0];

    feature_threshold <= wc_info[47:32];
    left_node <= wc_info[31:16];
    right_node <= wc_info[15:0];

end


always @(posedge clk) begin

//    if(reset == 1)
//    begin
//    $display("Heyo");
//    stage_decision = 0;
    
//    end
    
    case (state)
        2'b00: begin 
            stage_decision = 0;  
            if (fvalue_valid == 1 && !(op_done) == 1) begin
				stage_sum = stage_sum + out;
				op_done = 1;
				state = 2'b01;
            end
            else begin
            	state = state;
            end
        end
        
        
        2'b01:begin
//        $display("Testing");
			if(address == (no_of_features+address1-1)) begin
				final_stage_value = stage_sum;
//				stage_sum = 0;
//				if(final_stage_value == 0)
//				begin
//				stage_decision = 0;
//				end
////				
				if (stage_sum[15] == stage_threshold[15]) begin
				
//				 if(stage_sum[15] == 0)
//				 begin
				    $display("lol");
				// If both have the same sign, compare directly
				    if(reset == 1)
                        begin
                     
                        stage_decision = 0;
                        stage_sum = 0;
                        
                        end
					else if (stage_sum > stage_threshold) begin
						stage_decision = 1;
						 $display(stage_sum, "lol block");
					end 
					else begin
						stage_decision = 0;
					end
//				end
				
				end 
				else if (stage_sum[15] == 0) begin
				        $display("Joke");
				       
				        if(reset == 1)
                        begin
//                        $display("Heyo");
                        stage_decision = 0;
                         stage_sum = 0;
                        
                        end
                        
                        else
                        begin
						// final_stage_value is positive, stage_threshold is negative
						stage_decision = 1;
						 $display(stage_sum, "Joke block");
						end
				end 
				else begin
				        $display("Vedant");
						// final_stage_value is negative, stage_threshold is positive
						stage_decision = 0;
				end
				count1 = 0;
				
        
       		end
        
        	else begin
        	    stage_decision = 0;
				address = address + 1;
				op_done = 0;
				count = 0;      
				state = 2'b10;
			end
        end
        
        
        2'b10:
        begin
			if(count == 2'b11) begin
//			    address = address1;
				state = 2'b00;
			end
			
			else begin
				count = count + 1;
				state = 2'b10;
			end
        end
        
      
    endcase
end

assign stage_condition = stage_decision;

endmodule