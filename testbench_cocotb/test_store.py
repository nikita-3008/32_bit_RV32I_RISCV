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
async def test_store(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.i_rst.value = 1
    dut.rs1_val.value = 0
    dut.rs2_val.value = 0
    dut.imm.value = 0
    dut.store_control.value = 0

    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    str_ctrl = 0
    rs1 = 0
    rs2 = 0
    imm = 0
    for n in range(cnt):
        """ Assign Values to Input """

        await Timer(0.1,units="ns")

        if str_ctrl > 0:
            addr = (rs1 + imm)
            if addr != dut.mem_addr.value.integer:
                cocotb.log.info(f"Expected Addr: {addr} Actual output: {dut.mem_addr.value.integer} ; RS1_VAL: {rs1} ; IMM: {imm}")
                assert addr == dut.mem_addr.value.integer

            if str_ctrl == 1:
                if addr%4 == 0:
                    mem_write_data = lsb0*(2**0)
                    mem_byte_en = 1
                elif addr%4 == 1:
                    mem_write_data = lsb0*(2**8)
                    mem_byte_en = 2
                elif addr%4 == 2:
                    mem_write_data = lsb0*(2**16)
                    mem_byte_en = 4
                else:
                    mem_write_data = lsb0*(2**24)
                    mem_byte_en = 8
            elif str_ctrl == 2:
                if addr%4 == 0 or addr%4 == 1:
                    mem_write_data = lsb1*(2**8) + lsb0
                    mem_byte_en = 3
                else:
                    mem_write_data = (lsb1*(2**8) + lsb0)*(2**16)
                    mem_byte_en = 12
            else:
                mem_write_data = lsb3*(2**24) + lsb2*(2**16) + lsb1*(2**8) + lsb0
                mem_byte_en = 15

            assert 0 == dut.ignore_curr_inst.value.integer
            assert 1 == dut.stall_pc.value.integer
            assert 0 == dut.mem_rw_mode.value.integer
            assert mem_write_data == dut.mem_write_data.value.integer
            assert mem_byte_en == dut.mem_byte_en.value.integer

            await RisingEdge(dut.i_clk)
            dut.store_control.value = 0
            dut.rs1_val.value = 0
            dut.rs2_val.value = 0
            dut.imm.value = 0
            await Timer(0.1,units="ns")

            assert 1 == dut.ignore_curr_inst.value.integer
            assert 0 == dut.stall_pc.value.integer
            assert 1 == dut.mem_rw_mode.value.integer
            assert 0 == dut.mem_write_data.value.integer
            assert 0 == dut.mem_byte_en.value.integer

        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")

        assert 0 == dut.ignore_curr_inst.value.integer
        assert 0 == dut.stall_pc.value.integer
        assert 1 == dut.mem_rw_mode.value.integer
        assert 0 == dut.mem_write_data.value.integer
        assert 0 == dut.mem_byte_en.value.integer

        str_ctrl = random.randrange(0, 4)
        lsb0 = random.randrange(0, 2**8)
        lsb1 = random.randrange(0, 2**8)
        lsb2 = random.randrange(0, 2**8)
        lsb3 = random.randrange(0, 2**8)
        rs1 = random.randrange(0, 2**30)
        imm = random.randrange(0, 2**12)

        dut.rs1_val.value = rs1
        dut.rs2_val.value = lsb3*(2**24) + lsb2*(2**16) + lsb1*(2**8) + lsb0
        dut.imm.value = imm
        dut.store_control.value = str_ctrl
