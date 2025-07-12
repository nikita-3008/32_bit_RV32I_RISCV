import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_imm_inst(dut):
    cnt = 100

    ALU_NOP = 0
    ADDI  = 16
    XORI  = 17
    ORI   = 18
    ANDI  = 19
    SLLI  = 20
    SRLI  = 21
    SRAI  = 22
    SLTI  = 23
    SLTIU = 24


    """ TESTCASE """
    for n in range(cnt):
        rd = random.randrange(1, 2**5)
        rs1 = random.randrange(0, 2**5)
        func3 = random.randrange(0, 2**3)
        imm = random.randrange(0,2**12)
        if func3 == 5:
            imm = random.randrange(0,2**5)
            imm += (32)*random.randrange(0,2)
        if func3 == 1:
            imm = random.randrange(0,2**5)
        dut.instruction_code.value =  ((((imm)*(2**5) + rs1)*(2**3) + func3)*(2**5) + rd)
        await Timer(1,units="ns")
        if func3 == 0:
            alu_control = ADDI
        elif func3 == 4:
            alu_control = XORI
        elif func3 == 6:
            alu_control = ORI
        elif func3 == 7:
            alu_control = ANDI
        elif func3 == 1:
            alu_control = SLLI if (imm//2**5 == 0) else ALU_NOP
        elif func3 == 5:
            if imm//2**5 == 0:
                alu_control = SRLI
            elif imm//2**5 == 0x20:
                alu_control = SRAI
            else:
                alu_control = ALU_NOP
        elif func3 == 2:
            alu_control = SLTI
        elif func3 == 3:
            alu_control = SLTIU
        else:
            alu_control = ALU_NOP

        if rd != dut.rd.value.integer or rs1 != dut.rs1.value.integer or imm != dut.imm.value.integer or alu_control != dut.alu_control.value.integer:
            cocotb.log.info(f"Expected RD: {rd} Actual RD: {dut.rd.value.integer} ; Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer} ; Expected ALU Control: {alu_control} Actual ALU Control: {dut.alu_control.value.integer} ; Func3 : {func3}")

        assert rd == dut.rd.value.integer
        assert rs1 == dut.rs1.value.integer
        assert imm == dut.imm.value.integer
        assert alu_control == dut.alu_control.value.integer
