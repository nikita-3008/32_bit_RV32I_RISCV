import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_load_inst(dut):
    cnt = 100

    LD_NOP = 0
    LB = 1
    LH = 2
    LW = 3
    LBU = 4
    LHU = 5

    """ TESTCASE """
    for n in range(cnt):
        rd = random.randrange(1, 2**5)
        func3 = random.randrange(0, 2**3)
        rs1 = random.randrange(0, 2**5)
        imm = random.randrange(0,2**12)
        dut.instruction_code.value =  ((((imm)*(2**5) + rs1)*(2**3) + func3)*(2**5) + rd)
        await Timer(1,units="ns")
        if func3 == 0:
            load_control = LB
        elif func3 == 1:
            load_control = LH
        elif func3 == 2:
            load_control = LW
        elif func3 == 4:
            load_control = LBU
        elif func3 == 5:
            load_control = LHU
        else:
            load_control = LD_NOP

        if rd != dut.rd.value.integer or rs1 != dut.rs1.value.integer or imm != dut.imm.value.integer or load_control != dut.load_control.value.integer:
            cocotb.log.info(f"Expected RD: {rd} Actual RD: {dut.rd.value.integer} ; Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer} ; Expected load Control: {load_control} Actual load Control: {dut.load_control.value.integer} ; Func3 : {func3}")

        assert rd == dut.rd.value.integer
        assert rs1 == dut.rs1.value.integer
        assert imm == dut.imm.value.integer
        assert load_control == dut.load_control.value.integer
