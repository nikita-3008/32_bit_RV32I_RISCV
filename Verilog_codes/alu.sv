`include "processor_defines.sv"
`define SUBMODULE_DISABLE_WAVES_ALU_CORE
module alu(
    input logic [31:0] pc,
    input logic [31:0] imm,
    input logic [31:0] rs1_val,
    input logic [31:0] rs2_val,
    input logic [4:0] alu_control,
    output logic rd_write_control,
    output logic [31:0] rd_write_val
);

logic [31:0] rd_write_val_from_alu_core;
alu_core
I_alu_core(
	.rs1_val      (rs1_val),  
	.rs2_val      (rs2_val), 
	.alu_control  (alu_control), 
	.rd_write_val (rd_write_val_from_alu_core) 
);

always @ (*) begin
    rd_write_control = 1'b0;
    rd_write_val = 32'h0;

    if ((alu_control >= 1) && (alu_control <= 7)) begin
	rd_write_control = 1'b1;
	rd_write_val = rd_write_val_from_alu_core;
    end
    else begin
    	case (alu_control)
    	    `SRA: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val >>> rs2_val;
    	    end
    	    `SLT: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = $signed(rs1_val) < $signed(rs2_val);
    	    end
    	    `SLTU: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val < rs2_val;
    	    end

    	    `ADDI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val + imm;
    	    end
    	    `XORI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val ^ imm;
    	    end
    	    `ORI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val | imm;
    	    end
    	    `ANDI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val & imm;
    	    end
    	    `SLLI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val << {imm[4], imm[3], imm[2], imm[1], imm[0]};
    	    end
    	    `SRLI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val >> {imm[4], imm[3], imm[2], imm[1], imm[0]};
    	    end
    	    `SRAI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val >>> {imm[4], imm[3], imm[2], imm[1], imm[0]};
    	    end
    	    `SLTI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = $signed(rs1_val) < $signed(imm);
    	    end
    	    `SLTIU: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = rs1_val < imm;
    	    end

    	    `LUI: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = imm;
    	    end
    	    `AUIPC: begin
    	        rd_write_control = 1'b1;
    	        rd_write_val = pc + imm;
    	    end
    	endcase
    end
end

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
   	initial begin
        $dumpfile("./sim_build/alu.vcd");
        $dumpvars(0, alu);
    end
`endif


endmodule

