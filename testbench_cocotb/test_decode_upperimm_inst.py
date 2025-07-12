import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_upperimm_inst(dut):
    cnt = 100


    ALU_NOP = 0
    LUI = 28
    AUIPC = 29

    """ TESTCASE """
    for n in range(cnt):
        rd = random.randrange(1, 2**5)
        imm = random.randrange(0,2**20) * (2**12)
        opcode = random.choice([0, 55, 25])
        dut.instruction_code.value = imm + rd*(2**7) + opcode
        await Timer(1,units="ns")
        if opcode == 55:
            alu_control = LUI
        elif opcode == 23:
            alu_control = AUIPC
        else:
            alu_control = ALU_NOP

        if rd != dut.rd.value.integer or imm != dut.imm.value.integer or alu_control != dut.alu_control.value.integer:
            cocotb.log.info(f"Expected RD: {rd} Actual RD: {dut.rd.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer} ; Opcode : {opcode}")

        assert rd == dut.rd.value.integer
        assert imm == dut.imm.value.integer
        assert alu_control == dut.alu_control.value.integer
