import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_reg_inst(dut):
    cnt = 100

    ALU_NOP = 0
    ADD = 1
    SUB = 2
    XOR = 3
    OR  = 4
    AND = 5
    SLL = 6
    SRL = 7
    SRA = 8
    SLT = 9
    SLTU = 10

    """ TESTCASE """
    for n in range(cnt):
        rd = random.randrange(1, 2**5)
        rs1 = random.randrange(0, 2**5)
        rs2 = random.randrange(0, 2**5)
        func3 = random.randrange(0, 2**3)
        func7 = random.choice([0x0, 0x20])
        dut.instruction_code.value =  ((((func7*(2**5) + rs2)*(2**5) + rs1)*(2**3) + func3)*(2**5) + rd)
        await Timer(1,units="ns")
        if func3 == 0:
            if func7 == 0x00:
                alu_control = ADD
            elif func7 == 0x20:
                alu_control = SUB
            else:
                alu_control = ALU_NOP
        elif func3 == 4:
            alu_control = XOR if (func7 == 0x0) else ALU_NOP
        elif func3 == 6:
            alu_control = OR if (func7 == 0x0) else ALU_NOP
        elif func3 == 7:
            alu_control = AND if (func7 == 0x0) else ALU_NOP
        elif func3 == 1:
            alu_control = SLL if (func7 == 0x0) else ALU_NOP
        elif func3 == 5:
            if func7 == 0:
                alu_control = SRL
            elif func7 == 0x20:
                alu_control = SRA
            else:
                alu_control = ALU_NOP
        elif func3 == 2:
            alu_control = SLT if (func7 == 0x0) else ALU_NOP
        else:
            alu_control = SLTU if (func7 == 0x0) else ALU_NOP

        if rd != dut.rd.value.integer or rs1 != dut.rs1.value.integer or rs2 != dut.rs2.value.integer or alu_control != dut.alu_control.value.integer:
            cocotb.log.info(f"Expected RD: {rd} Actual RD: {dut.rd.value.integer} ; Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected RS2: {rs2} Actual RS2: {dut.rs2.value.integer} ; Expected ALU Control: {alu_control} Actual ALU Control: {dut.alu_control.value.integer} ; Func3 : {func3} ; Func7 : {func7}")

        assert rd == dut.rd.value.integer
        assert rs1 == dut.rs1.value.integer
        assert rs2 == dut.rs2.value.integer
        assert alu_control == dut.alu_control.value.integer
