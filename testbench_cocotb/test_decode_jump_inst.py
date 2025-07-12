import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_jump_inst(dut):
    cnt = 100
    JMP_NOP = 0
    JAL = 1
    JALR = 2

    """ TESTCASE """
    for n in range(cnt):
        opcode = random.choice([0, 111, 103])
        rd = random.randrange(1, 2**5)
        n19_n12 = random.randrange(0,2**(19-12+1))
        n11 = random.randrange(0,2)
        n10_n1 = random.randrange(0,2**(10-1+1))
        n20 = random.randrange(0,2)
        dut.instruction_code.value =  (((((n20)*(2**10) + n10_n1)*(2**1) + n11)*(2**(19-12+1)) + n19_n12)*(2**5) + rd)*(2**7) + opcode
        func3 = n19_n12%8
        await Timer(1,units="ns")
        if opcode == 111:
            jump_control = JAL
            imm = (((n20*(2**8) + n19_n12)*2 + n11)*2**(10)+n10_n1)*2
            rs1 = 0
        elif opcode == 103:
            if (func3 == 0):
                jump_control = JALR
                rs1 = n19_n12>>3
                imm = ((n20*(2**10) + n10_n1)*2 + n11)
            else:
                jump_control = JMP_NOP
                rs1 = 0
                imm = 0
        else:
            jump_control = JMP_NOP
            rs1 = 0
            imm = 0

        if rs1 != dut.rs1.value.integer or rd != dut.rd.value.integer or imm != dut.imm.value.integer or jump_control != dut.jump_control.value.integer:
            cocotb.log.info(f"Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected RD: {rd} Actual RD: {dut.rd.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer} ; Expected JUMP Control: {jump_control} Actual JUMP Control: {dut.jump_control.value.integer} ; Func3 : {func3} ; Opcode: {opcode}")

        assert rd == dut.rd.value.integer
        assert rs1 == dut.rs1.value.integer
        assert imm == dut.imm.value.integer
        assert jump_control == dut.jump_control.value.integer
