import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_store_inst(dut):
    cnt = 100
    STR_NOP = 0
    SB = 1
    SH = 2
    SW = 3

    """ TESTCASE """
    for n in range(cnt):
        rs1 = random.randrange(0, 2**5)
        rs2 = random.randrange(0, 2**5)
        func3 = random.randrange(0, 2**3)
        zerotofour = random.randrange(0,2**5)
        fivetoeleven = random.randrange(0,2**7)
        imm = fivetoeleven*(2**5) + zerotofour
        dut.instruction_code.value =  (((((fivetoeleven)*(2**5) + rs2)*(2**5) + rs1)*(2**3) + func3)*(2**5) + zerotofour)
        await Timer(1,units="ns")
        if func3 == 0:
            store_control = SB
        elif func3 == 1:
            store_control = SH
        elif func3 == 2:
            store_control = SW
        else:
            store_control = STR_NOP

        if rs1 != dut.rs1.value.integer or rs2 != dut.rs2.value.integer or imm != dut.imm.value.integer or store_control != dut.store_control.value.integer:
            cocotb.log.info(f"Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected RS2: {rs2} Actual RS2: {dut.rs2.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer}  ; Expected Store Control: {store_control} Actual Store Control: {dut.store_control.value.integer} ; Func3 : {func3}")

        assert rs2 == dut.rs2.value.integer
        assert rs1 == dut.rs1.value.integer
        assert store_control == dut.store_control.value.integer
        assert imm == dut.imm.value.integer
