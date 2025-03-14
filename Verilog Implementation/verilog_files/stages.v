module stages(
    input clk,
    output reg haar_decision
);


reg [2:0] count1 = 0;


reg reset = 0;
reg [15:0] no_of_weak_classifiers;
reg [15:0] stage_start_address;
reg [15:0] stage_address;
reg [1:0] stages_passed;
reg [1:0] state;
wire stage_valid;
wire [31:0] stagei;

blk_mem_gen_4 stage_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),       // input wire ena
  .wea(0),       // input wire [0 : 0] wea
  .addra(stage_address),  // input wire [15 : 0] addra
  .dina(0),      // input wire [31 : 0] dina
  .douta(stagei) // output wire [31 : 0] douta
);

Haar_stages h1(clk,reset,stage_start_address,no_of_weak_classifiers,stage_valid);

initial begin
    stage_address = 0;
    stage_start_address = 0;
    state = 2'b00;
    stages_passed = 0;
    haar_decision = 0;
end

always @(posedge clk) begin
    no_of_weak_classifiers <= stagei[31:16];
    stage_start_address <= stagei[15:0];
end

always @(posedge clk) begin
    case (state)
        2'b00: begin
            reset = 0;
            // Initial state: check if the current stage is valid
            if (stage_valid == 1) begin
//                reset <= 1;
                 stages_passed <= stages_passed + 1;
                state <= 2'b01;
            end else begin
                state <= 2'b00;  // Stay in the current stage if invalid
            end
        end

        2'b01: begin
            // If the stage is passed
            reset = 0;
              // Move to the next stage address
            if (stages_passed == 3) begin
//                stages_passed <= stages_passed + 1;
//                if (stages_passed == 1) begin
//                    stage_address <= stage_address + 1;  
//                    state <= 2'b00;
//                end else begin
//                    state <= 2'b10;  
//                end
             haar_decision <= 1;
               
            end 
            else begin
                // Reset to the beginning if the stage fails
               
                 count1 = 0;
                 stage_address <= stage_address + 1;
                 state <= 2'b10;
//                stage_start_address = 0; //changed here
//                state <= 2'b10;
            end
        end
        
        2'b10: begin
        
        reset = 1;
       
        if(count1 == 2'b10)
        begin
         
        state = 2'b00;
        
        end
        else
        begin
        
        count1 = count1 + 1;
        state = state;
        
        end
       end
//        2'b10: begin
//            // Final state, all stages passed
//            stage_address <= 0;
//            stages_passed <= 0;
//            state <= 2'b00;
//        end
    endcase
end

endmodulemodule stages(
    input clk,
    output reg haar_decision
);


reg [2:0] count1 = 0;


reg reset = 0;
reg [15:0] no_of_weak_classifiers;
reg [15:0] stage_start_address;
reg [15:0] stage_address;
reg [1:0] stages_passed;
reg [1:0] state;
wire stage_valid;
wire [31:0] stagei;

blk_mem_gen_4 stage_blk_ram (
  .clka(clk),    // input wire clka
  .ena(1),       // input wire ena
  .wea(0),       // input wire [0 : 0] wea
  .addra(stage_address),  // input wire [15 : 0] addra
  .dina(0),      // input wire [31 : 0] dina
  .douta(stagei) // output wire [31 : 0] douta
);

Haar_stages h1(clk,reset,stage_start_address,no_of_weak_classifiers,stage_valid);

initial begin
    stage_address = 0;
    stage_start_address = 0;
    state = 2'b00;
    stages_passed = 0;
    haar_decision = 0;
end

always @(posedge clk) begin
    no_of_weak_classifiers <= stagei[31:16];
    stage_start_address <= stagei[15:0];
end

always @(posedge clk) begin
    case (state)
        2'b00: begin
            reset = 0;
            // Initial state: check if the current stage is valid
            if (stage_valid == 1) begin
//                reset <= 1;
                 stages_passed <= stages_passed + 1;
                state <= 2'b01;
            end else begin
                state <= 2'b00;  // Stay in the current stage if invalid
            end
        end

        2'b01: begin
            // If the stage is passed
            reset = 0;
              // Move to the next stage address
            if (stages_passed == 3) begin
//                stages_passed <= stages_passed + 1;
//                if (stages_passed == 1) begin
//                    stage_address <= stage_address + 1;  
//                    state <= 2'b00;
//                end else begin
//                    state <= 2'b10;  
//                end
             haar_decision <= 1;
               
            end 
            else begin
                // Reset to the beginning if the stage fails
               
                 count1 = 0;
                 stage_address <= stage_address + 1;
                 state <= 2'b10;
//                stage_start_address = 0; //changed here
//                state <= 2'b10;
            end
        end
        
        2'b10: begin
        
        reset = 1;
       
        if(count1 == 2'b10)
        begin
         
        state = 2'b00;
        
        end
        else
        begin
        
        count1 = count1 + 1;
        state = state;
        
        end
       end
//        2'b10: begin
//            // Final state, all stages passed
//            stage_address <= 0;
//            stages_passed <= 0;
//            state <= 2'b00;
//        end
    endcase
end

endmodule