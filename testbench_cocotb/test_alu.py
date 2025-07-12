
import cocotb
from random import randint
import random
from cocotb.triggers import Timer


# convert a bits sized unsigned number to a signed number
def signed(num, bits):
    num = num % 2**bits
    if num >= 2**(bits-1):
        num = num - 2**bits
    return num

@cocotb.test()
async def test_alu(dut):
    # random.seed(10)
    for i in range(5000):
        pc    =   randint(0,2**8-1)
        imm   =   randint(0,2**8-1)
        imm_5b = imm%32
        rs1_val   =   randint(0,2**8-1)
        rs2_val   =   randint(0,2**8-1)
        alu_ctrl_list = [0,1,2,3,4,5,6,7,8,9,10, 16,17,18,19,20,21,22,23,24, 28,29, 30,31]
        if i < len(alu_ctrl_list)*100:
            alu_control = alu_ctrl_list[i//100]
        else:
            alu_control   =   random.choice(alu_ctrl_list)

        imm = imm_5b if (alu_control == 20 or alu_control == 21 or alu_control == 22) else imm
        rs2_val = rs2_val%5 if (alu_control == 6 or alu_control == 7) else rs2_val
    
        dut.pc.value    =   pc
        dut.imm.value   =   imm
        dut.rs1_val.value   =   rs1_val
        dut.rs2_val.value   = rs2_val
        dut.alu_control.value   =   alu_control
        res_valid = 0
        res = 0
        if (alu_control == 1): # ADD
            res_valid = 1
            res = rs1_val + rs2_val
        elif (alu_control == 2): # SUB
            res_valid = 1
            res = rs1_val - rs2_val
        elif (alu_control == 3): # XOR
            res_valid = 1
            res = rs1_val ^ rs2_val
        elif (alu_control == 4): # OR
            res_valid = 1
            res = rs1_val | rs2_val
        elif (alu_control == 5): # AND
            res_valid = 1
            res = rs1_val & rs2_val
        elif (alu_control == 6): # SLL
            res_valid = 1
            res = rs1_val << rs2_val
        elif (alu_control == 7): # SRL
            res_valid = 1
            res = rs1_val >> rs2_val
        elif (alu_control == 8): # SRA
            res_valid = 1
            res = signed(rs1_val, 32)// (2**rs2_val)
        elif (alu_control == 9): # SLT
            res_valid = 1
            res = signed(rs1_val, 32) < signed(rs2_val, 32)
        elif (alu_control == 10): # SLTU
            res_valid = 1
            res = rs1_val < rs2_val
        elif (alu_control == 16): # ADDI
            res_valid = 1
            res = rs1_val + imm
        elif (alu_control == 17): # XORI
            res_valid = 1
            res = rs1_val ^ imm
        elif (alu_control == 18): # ORI
            res_valid = 1
            res = rs1_val | imm
        elif (alu_control == 19): # ANDI
            res_valid = 1
            res = rs1_val & imm
        elif (alu_control == 20): # SLLI
            res_valid = 1 
            res = (rs1_val << imm_5b)
        elif (alu_control == 21): # SRLI
            res_valid = 1
            res = rs1_val >> imm_5b
        elif (alu_control == 22): # SRAI
            res_valid = 1
            res = signed(rs1_val, 32) // 2**imm_5b
        elif (alu_control == 23): # SLTI
            res_valid = 1
            res = signed(rs1_val,32) < signed(imm,32)
        elif (alu_control == 24): # SLTIU
            res_valid = 1
            res = rs1_val < imm
        elif (alu_control == 28): # LUI
            res_valid = 1
            res = imm
        elif (alu_control == 29): # AUIPC
            res_valid = 1
            res = pc + imm
  

        await Timer(1,units="ns")
        print(f"ID {i:4d} \t {alu_control:2d} {rs1_val} {rs2_val} {imm}\t \
              {res_valid} =  {dut.rd_write_control.value} \t \
              {signed(res,32)} = {dut.rd_write_val.value.signed_integer} ")
        assert res_valid == dut.rd_write_control.value
        assert signed(res,32) == dut.rd_write_val.value.signed_integer

# ***        
# // ALU Operations for reference
# `define ALU_NOP 5'd0
# `define ADD 5'd1
# `define SUB 5'd2
# `define XOR 5'd3
# `define OR 5'd4
# `define AND 5'd5
# `define SLL 5'd6
# `define SRL 5'd7
# `define SRA 5'd8
# `define SLT 5'd9
# `define SLTU 5'd10
# `define ADDI 5'd16
# `define XORI 5'd17
# `define ORI 5'd18
# `define ANDI 5'd19
# `define SLLI 5'd20
# `define SRLI 5'd21
# `define SRAI 5'd22
# `define SLTI 5'd23
# `define SLTIU 5'd24
# `define LUI 5'd28
# `define AUIPC 5'd29
# ***
