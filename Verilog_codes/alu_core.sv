// Instructions handled in alu_core
//      - ADD
//      - SUB
//      - XOR
//      - OR
//      - AND
//      - SLL
//      - SRL

`include "processor_defines.sv"
module alu_core(
    input logic [31:0] rs1_val,
    input logic [31:0] rs2_val,
    input logic [4:0] alu_control,
    output logic [31:0] rd_write_val
);

// Edit the code here begin ---------------------------------------------------

always @ (*)
   begin 
    rd_write_val=0;
    case(alu_control)
      5'd1 : rd_write_val=rs1_val+rs2_val ;
      5'd2 : rd_write_val=rs1_val-rs2_val ;
      5'd3 : rd_write_val=rs1_val^rs2_val ;
      5'd4 : rd_write_val=rs1_val|rs2_val ;
      5'd5 : rd_write_val=rs1_val&rs2_val ;
      5'd6 : rd_write_val=rs1_val<<rs2_val ;
      5'd7 : rd_write_val=rs1_val>>rs2_val ;
    endcase
   end




   
    
// Edit the code here end -----------------------------------------------------

/*
    Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES_ALU_CORE
    initial begin
        $dumpfile("./sim_build/alu_core.vcd");
        $dumpvars(0, alu_core);
    end
`endif

endmodule

