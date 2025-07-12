
`include "regfile.sv"
`include "alu.sv"
`include "alu_core.sv"
`include "load.sv"
`include "store.sv"
`include "branch.sv"
`include "jump.sv"

module ieu(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] pc,
    input logic [4:0] rs1,
    input logic [4:0] rs2,
    input logic [4:0] rd,
    input logic [31:0] imm,
    input logic [4:0] alu_control,
    input logic [2:0] load_control,
    input logic [2:0] store_control,
    input logic [2:0] branch_control,
    input logic [1:0] jump_control,
    input logic [31:0] mem_read_data,
    output logic pc_update_control,
    output logic [31:0] pc_update_val,
    output logic stall_pc,
    output logic mem_rw_mode,
    output logic [31:0] mem_addr,
    output logic [31:0] mem_write_data,
    output logic [3:0] mem_byte_en,
    output logic ignore_curr_inst 
);

logic rd_write_control;
logic [31:0] rd_write_val;
logic [31:0] rs1_val;
logic [31:0] rs2_val;
logic [4:0] rd_muxed;

regfile inst_regfile(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .rs1                (rs1),
    .rs2                (rs2),
    .rd                 (rd_muxed),
    .rd_write_control   (rd_write_control),
    .rd_write_val       (rd_write_val),
    .rs1_val            (rs1_val),
    .rs2_val            (rs2_val)
);

logic alu_rd_write_control;
logic [31:0] alu_rd_write_val;

alu inst_alu(
    .pc                 (pc),
    .imm                (imm),
    .rs1_val            (rs1_val),
    .rs2_val            (rs2_val),
    .alu_control        (alu_control),
    .rd_write_control   (alu_rd_write_control),
    .rd_write_val       (alu_rd_write_val)
);

logic branch_pc_update_control;
logic [31:0] branch_pc_update_val;
logic branch_ignore_curr_inst;

branch inst_branch(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .pc                 (pc),
    .imm                (imm),
    .rs1_val            (rs1_val),
    .rs2_val            (rs2_val),
    .branch_control     (branch_control),
    .pc_update_control  (branch_pc_update_control),
    .pc_update_val      (branch_pc_update_val),
    .ignore_curr_inst   (branch_ignore_curr_inst)
);

logic jump_rd_write_control;
logic [31:0] jump_rd_write_val;
logic jump_pc_update_control;
logic [31:0] jump_pc_update_val;
logic jump_ignore_curr_inst;

jump inst_jump(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .pc                 (pc),
    .imm                (imm),
    .rs1_val            (rs1_val),
    .jump_control       (jump_control),
    .rd_write_control   (jump_rd_write_control),
    .rd_write_val       (jump_rd_write_val),
    .pc_update_control  (jump_pc_update_control),
    .pc_update_val      (jump_pc_update_val),
    .ignore_curr_inst   (jump_ignore_curr_inst)
);

logic load_stall_pc;
logic load_ignore_curr_inst;
logic load_rd_write_control;
logic [4:0] load_rd_out;
logic [31:0] load_rd_write_val;
logic load_mem_rw_mode;
logic [31:0] load_mem_addr;

load inst_load(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .rs1_val            (rs1_val),
    .imm                (imm),
    .mem_data           (mem_read_data),
    .rd_in              (rd),
    .load_control       (load_control),
    .stall_pc           (load_stall_pc),
    .ignore_curr_inst   (load_ignore_curr_inst),
    .rd_write_control   (load_rd_write_control),
    .rd_out             (load_rd_out),
    .rd_write_val       (load_rd_write_val),
    .mem_rw_mode        (load_mem_rw_mode),
    .mem_addr           (load_mem_addr)
);

logic store_stall_pc;
logic store_ignore_curr_inst;
logic store_mem_rw_mode;
logic [31:0] store_mem_addr;

store inst_store(
    .i_clk              (i_clk),
    .i_rst              (i_rst),
    .rs1_val            (rs1_val),
    .rs2_val            (rs2_val),
    .imm                (imm),
    .store_control      (store_control),
    .stall_pc           (store_stall_pc),
    .ignore_curr_inst   (store_ignore_curr_inst),
    .mem_rw_mode        (store_mem_rw_mode),
    .mem_addr           (store_mem_addr),
    .mem_write_data     (mem_write_data),
    .mem_byte_en        (mem_byte_en)
);

always @ (*) begin
    if (load_ignore_curr_inst)
        rd_muxed = load_rd_out;
    else
        rd_muxed = rd;

    rd_write_control = alu_rd_write_control | jump_rd_write_control | load_rd_write_control;
    rd_write_val = alu_rd_write_val | jump_rd_write_val | load_rd_write_val;
    
    pc_update_control = branch_pc_update_control | jump_pc_update_control;
    pc_update_val = branch_pc_update_val  | jump_pc_update_val;
    stall_pc = load_stall_pc | store_stall_pc;
    ignore_curr_inst = branch_ignore_curr_inst | jump_ignore_curr_inst | load_ignore_curr_inst | store_ignore_curr_inst;
    
    mem_rw_mode = load_mem_rw_mode & store_mem_rw_mode;
    mem_addr = load_mem_addr | store_mem_addr;
end

endmodule
