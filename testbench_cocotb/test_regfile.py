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
async def test_regfile(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.i_rst.value = 1
    dut.rs1.value = 0
    dut.rs2.value = 0
    dut.rd.value = 0
    dut.rd_write_control.value = 0
    dut.rd_write_val.value = 0

    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    rs1 = 0
    rs2 = 0
    rd = 0
    rd_write_control = 0
    rd_write_val = 0
    arr = [0]*32
    for n in range(cnt):
        """ Assign Values to Input """

        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")
        assert arr[rs1] == dut.rs1_val.value.integer
        assert arr[rs2] == dut.rs2_val.value.integer

        rs1 = random.randrange(0, 2**5)
        rs2 = random.randrange(0, 2**5)
        rd  = random.randrange(0, 2**5)
        rd_write_control = random.randrange(0, 2)
        rd_write_val = random.randrange(0, 2**32)

        if (rd_write_control == 1 and rd > 0):
            arr[rd] = rd_write_val

        dut.rs1.value = rs1
        dut.rs2.value = rs2
        dut.rd.value = rd
        dut.rd_write_control.value = rd_write_control
        dut.rd_write_val.value = rd_write_val
