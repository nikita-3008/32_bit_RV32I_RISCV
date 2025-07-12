
`include "decode_reg_inst.sv"
`include "decode_imm_inst.sv"
`include "decode_load_inst.sv"
`include "decode_store_inst.sv"
`include "decode_branch_inst.sv"
`include "decode_jump_inst.sv"
`include "decode_upperimm_inst.sv"

module idu(
    input logic [31:0] instruction_code,
    output logic [4:0] rs1,
    output logic [4:0] rs2,
    output logic [4:0] rd,
    output logic [31:0] imm,
    output logic [4:0] alu_control,
    output logic [2:0] load_control,
    output logic [2:0] store_control,
    output logic [2:0] branch_control,
    output logic [1:0] jump_control
);

logic [4:0] reg_inst_rs1;
logic [4:0] reg_inst_rs2;
logic [4:0] reg_inst_rd;
logic [4:0] reg_inst_alu_control;

decode_reg_inst inst_decode_reg_instruction(
    .instruction_code   (instruction_code[31:7]),
    .rs1                (reg_inst_rs1),
    .rs2                (reg_inst_rs2),
    .rd                 (reg_inst_rd),
    .alu_control        (reg_inst_alu_control)
);

logic [4:0] imm_inst_rs1;
logic [4:0] imm_inst_rd;
logic [11:0] imm_inst_imm;
logic [4:0] imm_inst_alu_control;

decode_imm_inst inst_decode_imm_instruction(
    .instruction_code   (instruction_code[31:7]),
    .rs1                (imm_inst_rs1),
    .rd                 (imm_inst_rd),
    .imm                (imm_inst_imm),
    .alu_control        (imm_inst_alu_control)
);

logic [4:0] load_inst_rs1;
logic [4:0] load_inst_rd;
logic [11:0] load_inst_imm;
logic [2:0] w_load_control;

decode_load_inst inst_decode_load_instruction(
    .instruction_code   (instruction_code[31:7]),
    .rs1                (load_inst_rs1),
    .rd                 (load_inst_rd),
    .imm                (load_inst_imm),
    .load_control       (w_load_control)
);

logic [4:0] store_inst_rs1;
logic [4:0] store_inst_rs2;
logic [11:0] store_inst_imm;
logic [2:0] w_store_control;

decode_store_inst inst_decode_store_instruction(
    .instruction_code   (instruction_code[31:7]),
    .rs1                (store_inst_rs1),
    .rs2                (store_inst_rs2),
    .imm                (store_inst_imm),
    .store_control      (w_store_control)
);

logic [4:0] branch_inst_rs1;
logic [4:0] branch_inst_rs2;
logic [12:0] branch_inst_imm;
logic [2:0] w_branch_control;

decode_branch_inst inst_decode_branch_instruction(
    .instruction_code   (instruction_code[31:7]),
    .rs1                (branch_inst_rs1),
    .rs2                (branch_inst_rs2),
    .imm                (branch_inst_imm),
    .branch_control     (w_branch_control)
);

logic [4:0] jump_inst_rd;
logic [4:0] jump_inst_rs1;
logic [20:0] jump_inst_imm;
logic [1:0] w_jump_control;

decode_jump_inst inst_decode_jump_instruction(
    .instruction_code   (instruction_code),
    .rd                 (jump_inst_rd),
    .rs1                (jump_inst_rs1),
    .imm                (jump_inst_imm),
    .jump_control       (w_jump_control)
);

logic [4:0] upperimm_inst_rd;
logic [31:0] upperimm_inst_imm;
logic [4:0] upperimm_inst_alu_control;

decode_upperimm_inst inst_decode_upperimm_instruction(
    .instruction_code   (instruction_code),
    .rd                 (upperimm_inst_rd),
    .imm                (upperimm_inst_imm),
    .alu_control        (upperimm_inst_alu_control)
);

always @ (*) begin
    rs1 = 32'h0;
    rs2 = 32'h0;
    rd = 32'h0;
    imm = 32'h0;
    alu_control = `ALU_NOP;
    load_control = `LD_NOP;
    store_control = `STR_NOP;
    branch_control = `BR_NOP;
    jump_control = `JMP_NOP;
    case (instruction_code[6:0])
        `OP_REG: begin
            rs1 = reg_inst_rs1;
            rs2 = reg_inst_rs2;
            rd = reg_inst_rd;
            alu_control = reg_inst_alu_control;
        end
        `OP_IMM: begin
            rs1 = imm_inst_rs1;
            rd = imm_inst_rd;
            imm = imm_inst_imm;
            alu_control = imm_inst_alu_control;
        end
        `OP_LOAD: begin
            rs1 = load_inst_rs1;
            rd = load_inst_rd;
            imm = load_inst_imm;
            load_control = w_load_control;
        end
        `OP_STORE: begin
            rs1 = store_inst_rs1;
            rs2 = store_inst_rs2;
            imm = store_inst_imm;
            store_control = w_store_control;
        end
        `OP_BRANCH: begin
            rs1 = branch_inst_rs1;
            rs2 = branch_inst_rs2;
            imm = branch_inst_imm;
            branch_control = w_branch_control;
        end
        `OP_JAL: begin
            rd = jump_inst_rd;
            imm = jump_inst_imm;
            jump_control = w_jump_control;
        end
        `OP_JALR: begin
            rd = jump_inst_rd;
            rs1 = jump_inst_rs1;
            imm = jump_inst_imm;
            jump_control = w_jump_control;
        end
        `OP_LUI: begin
            rd = upperimm_inst_rd;
            imm = upperimm_inst_imm;
            alu_control = upperimm_inst_alu_control;
        end
        `OP_AUIPC: begin
            rd = upperimm_inst_rd;
            imm = upperimm_inst_imm;
            alu_control = upperimm_inst_alu_control;
        end
    endcase
end


endmodule
