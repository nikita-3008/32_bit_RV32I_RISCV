import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_branch_inst(dut):
    cnt = 100

    BR_NOP =  0
    BEQ =  1
    BNE =  2
    BLT =  3
    BGE =  4
    BLTU =  5
    BGEU =  6

    """ TESTCASE """
    for n in range(cnt):

        rs1 = random.randrange(0, 2**5)
        rs2 = random.randrange(0, 2**5)
        func3 = random.randrange(0, 2**3)
        eleven = random.randrange(0,2)
        onetofour = random.randrange(0,2**4)
        fivetoten = random.randrange(0,2**6)
        twelve = random.randrange(0,2)
        imm = 2*(onetofour + 2**4*(fivetoten + 2**6*(eleven + 2*twelve)))
        dut.instruction_code.value = ((((((twelve)*(2**6)+fivetoten)*(2**5)+rs2)*(2**5)+rs1)*(2**3) +func3)*(2**4) + onetofour)*2 + eleven

        await Timer(1,units="ns")
        if func3 == 0:
            branch_control = BEQ
        elif func3 == 1:
            branch_control = BNE
        elif func3 == 4:
            branch_control = BLT
        elif func3 == 5:
            branch_control = BGE
        elif func3 == 6:
            branch_control = BLTU
        elif func3 == 7:
            branch_control = BGEU
        else:
            branch_control = BR_NOP

        if rs2 != dut.rs2.value.integer or rs1 != dut.rs1.value.integer or imm != dut.imm.value.integer or branch_control != dut.branch_control.value.integer:
            cocotb.log.info(f"Expected Rs2: {rs2} Actual Rs2: {dut.rs2.value.integer} ; Expected RS1: {rs1} Actual RS1: {dut.rs1.value.integer} ; Expected RS2: {rs2} Actual RS2: {dut.rs2.value.integer} ; Expected IMM: {imm} Actual IMM: {dut.imm.value.integer} ; Expected Branch Control: {branch_control} Actual Branch Control: {dut.branch_control.value.integer} ; Func3 : {func3}; ")

        assert rs2 == dut.rs2.value.integer
        assert rs1 == dut.rs1.value.integer
        assert branch_control == dut.branch_control.value.integer
        assert imm == dut.imm.value.integer
