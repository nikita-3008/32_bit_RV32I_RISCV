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
async def test_jump(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.i_rst.value = 1
    dut.rs1_val.value = 0
    dut.pc.value = 0
    dut.imm.value = 0
    dut.jump_control.value = 0

    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    jmp_ctrl = 0
    pc = 0
    rs1 = 0
    imm = 0
    for n in range(cnt):
        """ Assign Values to Input """

        await Timer(0.1,units="ns")

        if jmp_ctrl > 0:
            if jmp_ctrl == 1:
                pc_update_val = (pc + imm)
            else:
                pc_update_val = (rs1 + imm)

            assert 0 == dut.ignore_curr_inst.value.integer
            assert 1 == dut.rd_write_control.value.integer
            assert (pc+4) == dut.rd_write_val.value.integer
            assert pc_update_val == dut.pc_update_val.value.integer
            assert 1 == dut.pc_update_control.value.integer

            await RisingEdge(dut.i_clk)
            dut.pc.value = pc + 4
            dut.rs1_val.value = 0
            dut.imm.value = 0
            dut.jump_control.value = 0
            await Timer(0.1,units="ns")
            assert 1 == dut.ignore_curr_inst.value.integer
            assert 0 == dut.rd_write_control.value.integer
            assert 0 == dut.rd_write_val.value.integer
            assert 0 == dut.pc_update_val.value.integer
            assert 0 == dut.pc_update_control.value.integer

        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")
        assert 0 == dut.ignore_curr_inst.value.integer
        assert 0 == dut.rd_write_control.value.integer
        assert 0 == dut.rd_write_val.value.integer
        assert 0 == dut.pc_update_val.value.integer
        assert 0 == dut.pc_update_control.value.integer

        jmp_ctrl = random.randrange(0, 3)
        pc = random.randrange(0, 2**30)
        rs1 = random.randrange(0, 2**30)
        imm = random.randrange(0, 2**12)

        dut.pc.value = pc
        dut.rs1_val.value = rs1
        dut.imm.value = imm
        dut.jump_control.value = jmp_ctrl
