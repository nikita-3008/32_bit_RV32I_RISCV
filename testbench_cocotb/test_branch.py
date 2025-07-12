import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

async def start_clock(clk_pin):
    clk_pin.value = 0
    await Timer(5, "ns")
    cocotb.start_soon(Clock(clk_pin, 1, units="ns").start())

async def reset_dut(dut):
    """ Reset the DUT """
    await FallingEdge(dut.i_clk)
    dut.i_rst.value = 0
    for n in range(2):
        await RisingEdge(dut.i_clk)
    dut.i_rst.value = 1

@cocotb.test()
async def test_branch(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.i_rst.value = 1
    dut.rs1_val.value = 0
    dut.rs2_val.value = 0
    dut.pc.value = 0
    dut.imm.value = 0
    dut.branch_control.value = 0

    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    branch_control = 0
    pc = 0
    rs1 = 0
    rs2 = 0
    imm = 0
    for n in range(cnt):
        """ Assign Values to Input """

        await Timer(0.1,units="ns")

        if branch_control > 0:
            if branch_control == 1:
                branch_condn = (rs1 == rs2)
            elif branch_control == 2:
                branch_condn = (rs1 != rs2)
            elif branch_control == 3:
                branch_condn = rs1 < rs2
            elif branch_control == 4:
                branch_condn = rs1 >= rs2
            elif branch_control == 5:
                branch_condn = rs1 < rs2
            elif branch_control == 6:
                branch_condn = rs1 >= rs2
            else:
                branch_condn = 0

            if branch_condn == 1:
                assert 0 == dut.ignore_curr_inst.value.integer
                assert (pc+imm) == dut.pc_update_val.value.integer
                assert 1 == dut.pc_update_control.value.integer

                await RisingEdge(dut.i_clk)
                dut.pc.value = pc + imm
                dut.rs1_val.value = 0
                dut.rs2_val.value = 0
                dut.imm.value = 0
                dut.branch_control.value = 0
                await Timer(0.1,units="ns")
                assert 1 == dut.ignore_curr_inst.value.integer
                assert 0 == dut.pc_update_val.value.integer
                assert 0 == dut.pc_update_control.value.integer

        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")
        assert 0 == dut.ignore_curr_inst.value.integer
        assert 0 == dut.pc_update_val.value.integer
        assert 0 == dut.pc_update_control.value.integer

        branch_control = random.randrange(0, 8)
        pc = random.randrange(0, 2**30)
        rs1 = random.randrange(0, 2**30)
        rs2 = rs1 + random.choice([-1, 0, 1])
        imm = random.randrange(0, 2**12)

        dut.pc.value = pc
        dut.rs1_val.value = rs1
        dut.rs2_val.value = rs2
        dut.imm.value = imm
        dut.branch_control.value = branch_control
