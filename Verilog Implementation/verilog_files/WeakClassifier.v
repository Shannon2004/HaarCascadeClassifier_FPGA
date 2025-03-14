module WeakClassifier(
    input clk,
    input op_done,
    input [15:0] A1,
    input [15:0] B1,
    input [15:0] C1,
    input [15:0] D1,
    input [15:0] weight1,
    input [15:0] A2,
    input [15:0] B2,
    input [15:0] C2,
    input [15:0] D2,
    input [15:0] weight2,
    input [15:0] A3,
    input [15:0] B3,
    input [15:0] C3,
    input [15:0] D3,
    input [15:0] weight3,
    input [15:0] feature_threshold,
    input [15:0] left_node,
    input [15:0] right_node,
    output [15:0] feature_value,
    output reg fvalue_valid
);








reg [15:0] I1_inter;
reg [15:0] I2_inter;
reg [15:0] I3_inter;

reg [15:0] I1_inter1 ;
reg [15:0] I2_inter1 ;
reg [15:0] I3_inter1;

reg [15:0] I1_inter2 ;
reg [15:0] I2_inter2;
reg [15:0] I3_inter2;


reg [15:0] temp ;
reg [15:0] temp1;
reg [15:0] temp2 ;


reg[15:0] temp4 ;
reg[15:0] temp5 ;

reg [15:0] weighted_intensity1;
reg [15:0] weighted_intensity2;
reg [15:0] weighted_intensity3;

reg [15:0] feature_temp_value;

wire temp5_sign;
assign temp5_sign = temp5[15]; // MSB is the sign bit



initial 
begin
  
  feature_temp_value = 15'b0;
  fvalue_valid = 0;

end





//dsp_macro_0 dsp1 (
//  .CLK(clk),  // input wire CLK
//  .A(temp),      // input wire [24 : 0] A
//  .B(weight1),      // input wire [5 : 0] B
//  .P(weighted_intensity1)      // output wire [30 : 0] P
//);

//dsp_macro_0 dsp2 (
//  .CLK(clk),  // input wire CLK
//  .A(temp1),      // input wire [24 : 0] A
//  .B(weight2),      // input wire [5 : 0] B
//  .P(weighted_intensity2)      // output wire [30 : 0] P
//);

//dsp_macro_0 dsp3 (
//  .CLK(clk),  // input wire CLK
//  .A(temp2),      // input wire [24 : 0] A
//  .B(weight3),      // input wire [5 : 0] B
//  .P(weighted_intensity3)      // output wire [30 : 0] P
//);






always @(posedge clk)
begin

I1_inter = A1+D1;
I2_inter = B1 + C1;
I1_inter1 = A2+D2;
I2_inter1 = B2 + C2;
I1_inter2 = A3+D3;
I2_inter2 = B3 + C3;


temp = I1_inter-I2_inter;
temp1 = I1_inter1-I2_inter1;
temp2 = I1_inter2-I2_inter2;


weighted_intensity1 = temp*weight1;
weighted_intensity2 = temp1*weight2;
weighted_intensity3 = temp2*weight3;

temp4 = weighted_intensity1 + weighted_intensity2;
temp5 = temp4 + weighted_intensity3;
  if(op_done == 1)
  begin
      fvalue_valid = 0;
  end
  
  else if(A1 == 0 && B1 == 0 && C1 == 0 && D1 == 0 && weight1 == 0)
  begin
  
  fvalue_valid = 0;
  
  end
  
  else begin
        // Check sign of temp5 and feature_threshold using the 15th bit (MSB)
        
        
        if (temp5[15] == feature_threshold[15]) begin
        
//        if(temp[15] == 0)
//        begin
            // Both numbers have the same sign; compare directly
            if (temp5 >= feature_threshold) begin
                feature_temp_value = left_node;
                fvalue_valid = 1;
            end else if(temp5 < feature_threshold) begin
                feature_temp_value = right_node;
                fvalue_valid = 1;
            end
//        end
      
        end else if (temp5[15] == 1) begin
            // temp5 is negative, feature_threshold is positive
            feature_temp_value = right_node;
            fvalue_valid = 1;
        end else if(temp5[15] == 0) begin
            // temp5 is positive, feature_threshold is negative
            feature_temp_value = left_node;
            fvalue_valid = 1;
        end

    end



	
	

end






assign feature_value = feature_temp_value;






endmodule