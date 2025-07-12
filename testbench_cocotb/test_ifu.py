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
async def test_ifu(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.stall_pc.value = 0
    dut.pc_update_control.value = 0
    dut.pc_update_val.value = 0
    dut.i_rst.value = 1
    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    stall = 0
    update_control = 0
    update_val = 0
    pc_golden = 0
    for n in range(cnt):
        """ Assign Values to Input """
        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")

        if stall == 0:
            if update_control == 0:
                pc_golden = pc_golden + 4
            else:
                pc_golden = update_val
        else:
            pc_golden = pc_golden

        cocotb.log.info(f"Expected_output: {pc_golden} Actual output: {dut.pc.value.integer}")
        assert pc_golden == dut.pc.value.integer

        stall = random.randrange(0, 2)
        update_control = random.randrange(0, 2)
        update_val = pc_golden + random.randrange(0, 128, 4)

        dut.stall_pc.value = stall
        dut.pc_update_control.value = update_control
        dut.pc_update_val.value = update_val
