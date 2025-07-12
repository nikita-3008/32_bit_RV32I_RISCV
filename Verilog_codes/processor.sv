
`define SUBMODULE_DISABLE_WAVES
`define SUBMODULE_DISABLE_WAVES_ALU_CORE

`include "processor_defines.sv"
`include "ifu.sv"
`include "inst_data_arbiter.sv"
`include "mem.sv"
`include "idu.sv"
`include "ieu.sv"

module processor(
    input logic i_clk,
    input logic i_rst
);

logic stall_pc;
logic pc_update_control;
logic [31:0] pc_update_val;
logic [31:0] pc;
logic [31:0] prev_pc;

ifu inst_ifu(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .stall_pc           (stall_pc),
    .pc_update_control  (pc_update_control),
    .pc_update_val      (pc_update_val),
    .pc                 (pc),
    .prev_pc            (prev_pc)
);

logic mem_rw_mode;
logic [31:0] mem_addr;
logic [31:0] mem_read_data;
logic [31:0] mem_write_data;
logic [31:0] instruction_code;
logic [3:0] mem_byte_en;
logic ignore_curr_inst;
logic [31:0] from_mem_data;
logic [31:0] to_mem_addr;
logic to_mem_rw_mode;
logic [31:0] to_mem_write_data;
logic [3:0] to_mem_byte_en;

inst_data_arbiter inst_intruction_data_arbiter(
    .inst_addr          (pc),
    .stall_pc           (stall_pc),
    .mem_addr           (mem_addr),
    .mem_rw_mode        (mem_rw_mode),
    .mem_write_data     (mem_write_data),
    .mem_byte_en        (mem_byte_en),
    .ignore_curr_inst   (ignore_curr_inst),
    .from_mem_data      (from_mem_data),
    .instruction_code   (instruction_code),
    .mem_read_data      (mem_read_data),
    .to_mem_addr        (to_mem_addr),
    .to_mem_rw_mode     (to_mem_rw_mode),
    .to_mem_write_data  (to_mem_write_data),
    .to_mem_byte_en     (to_mem_byte_en)
);

mem inst_mem(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .in_mem_addr        (to_mem_addr[`MEM_ADDR_WD+1:2]),
    .in_mem_re_web      (to_mem_rw_mode),
    .in_mem_write_data  (to_mem_write_data),
    .in_mem_byte_en     (to_mem_byte_en),
    .out_mem_data       (from_mem_data)
);

logic [4:0] rs1;
logic [4:0] rs2;
logic [4:0] rd;
logic [31:0] imm;
logic [4:0] alu_control;
logic [2:0] load_control;
logic [2:0] store_control;
logic [2:0] branch_control;
logic [1:0] jump_control;

idu inst_idu(
    .instruction_code   (instruction_code),
    .rs1                (rs1),
    .rs2                (rs2),
    .rd                 (rd),
    .imm                (imm),
    .alu_control        (alu_control),
    .load_control       (load_control),
    .store_control      (store_control),
    .branch_control     (branch_control),
    .jump_control       (jump_control)
);


ieu inst_ieu(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .pc                 (prev_pc),
    .rs1                (rs1),
    .rs2                (rs2),
    .rd                 (rd),
    .imm                (imm),
    .alu_control        (alu_control),
    .load_control       (load_control),
    .store_control      (store_control),
    .branch_control     (branch_control),
    .jump_control       (jump_control),
    .mem_read_data      (mem_read_data),
    .pc_update_control  (pc_update_control),
    .pc_update_val      (pc_update_val),
    .stall_pc           (stall_pc),
    .mem_rw_mode        (mem_rw_mode),
    .mem_addr           (mem_addr),
    .mem_write_data     (mem_write_data),
    .mem_byte_en        (mem_byte_en),
    .ignore_curr_inst   (ignore_curr_inst)
);


/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

integer i;

`ifndef DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/processor.vcd");
        $dumpvars(0, processor);
        for (i=0; i<32; i=i+1) begin
            $dumpvars(0, processor.inst_ieu.inst_regfile.regs[i]);
        end
        for (i=0; i<1024; i=i+1) begin
            $dumpvars(0, processor.inst_mem.memory_reg[i]);
        end
    end
`endif

endmodule
