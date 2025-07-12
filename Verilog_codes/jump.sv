
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module jump(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] pc,
    input logic [31:0] imm,
    input logic [31:0] rs1_val,
    input logic [1:0] jump_control,
    output logic rd_write_control,
    output logic [31:0] rd_write_val,
    output logic pc_update_control,
    output logic [31:0] pc_update_val,
    output logic ignore_curr_inst
);

// Edit the code here begin ---------------------------------------------------

    // assign rd_write_control = 'b0;
    // assign rd_write_val = 'b0;
    // assign pc_update_control = 'b0;
    // assign pc_update_val = 'b0;
    // assign ignore_curr_inst = 'b0;

    always @ (posedge i_clk or negedge i_rst)
      begin
        if (~i_rst)
        begin
           ignore_curr_inst<=1'b0;
            
        end
        else if (jump_control==`JAL | `JALR)
          ignore_curr_inst<=pc_update_control;
          

            
      end
 always_comb
 begin       
  if (jump_control==`JAL)
  begin
            rd_write_control=1'b1;
            rd_write_val=pc+4;
            pc_update_control=1'b1;
            pc_update_val=pc+imm;
           
        end
 else if (jump_control==`JALR)
 begin
            rd_write_control=1'b1;
            rd_write_val=pc+4;
            pc_update_control=1'b1;
            pc_update_val=rs1_val+imm;
 end
  else begin
      rd_write_control=1'b0;
            rd_write_val=0;
            pc_update_control=1'b0;
            pc_update_val=0;
 end
 end
             
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/jump.vcd");
        $dumpvars(0, jump);
    end
`endif

endmodule
