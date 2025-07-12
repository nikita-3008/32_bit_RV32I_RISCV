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
async def test_load(dut):
    cnt = 100
    """ Assign Initial to Input """
    dut.i_rst.value = 1
    dut.rs1_val.value = 0
    dut.imm.value = 0
    dut.mem_data.value = 0
    dut.rd_in.value = 0
    dut.load_control.value = 0

    """ Start Clock and Give Reset """
    await start_clock(dut.i_clk)
    await reset_dut(dut)

    """ TESTCASE """
    ld_ctrl = 0
    rd = 0
    rs1 = 0
    imm = 0
    for n in range(cnt):
        """ Assign Values to Input """

        await Timer(0.1,units="ns")

        if ld_ctrl > 0:
            addr = (rs1 + imm)
            if addr != dut.mem_addr.value.integer:
                cocotb.log.info(f"Expected Addr: {(addr//4)} Actual output: {dut.mem_addr.value.integer} ; RS1_VAL: {rs1} ; IMM: {imm}")
                assert addr == dut.mem_addr.value.integer

            assert 0 == dut.ignore_curr_inst.value.integer
            assert 1 == dut.stall_pc.value.integer
            assert 0 == dut.rd_write_control.value.integer
            assert 0 == dut.rd_write_val.value.integer
            assert 0 == dut.rd_out.value.integer
            assert 1 == dut.mem_rw_mode.value.integer

            await RisingEdge(dut.i_clk)
            lsb0 = random.randrange(0, 2**8)
            lsb1 = random.randrange(0, 2**8)
            lsb2 = random.randrange(0, 2**8)
            lsb3 = random.randrange(0, 2**8)
            dut.mem_data.value = (lsb3*(2**24) + lsb2*(2**16) + lsb1*(2**8) + lsb0)
            dut.load_control.value = 0
            dut.rd_in.value = 0
            dut.rs1_val.value = 0
            dut.imm.value = 0
            await Timer(0.1,units="ns")


            if ld_ctrl == 1:
                if (addr%4 == 0):
                    val = lsb0
                    msbs =  4294967040 if (val >= 2**7) else 0
                    mem_write_val = msbs + val
                elif (addr%4 == 1):
                    val = lsb1
                    msbs =  4294967040 if (val >= 2**7) else 0
                    mem_write_val = msbs + val
                elif (addr%4 == 2):
                    val = lsb2
                    msbs =  4294967040 if (val >= 2**7) else 0
                    mem_write_val = msbs + val
                else:
                    val = lsb3
                    msbs =  4294967040 if (val >= 2**7) else 0
                    mem_write_val = msbs + val
            elif ld_ctrl == 2:
                if (addr%4 == 0 or addr%4 == 1):
                    val = lsb1
                    msbs =  4294901760 if (val >= 2**7) else 0
                    mem_write_val = msbs + lsb1*(2**8) + lsb0
                else:
                    val = lsb3
                    msbs =  4294901760 if (val >= 2**7) else 0
                    mem_write_val = msbs + lsb3*(2**8) + lsb2
            elif ld_ctrl == 3:
                mem_write_val = (lsb3*(2**24) + lsb2*(2**16) + lsb1*(2**8) + lsb0)
            elif ld_ctrl == 4:
                if (addr%4 == 0):
                    mem_write_val = lsb0
                elif (addr%4 == 1):
                    mem_write_val = lsb1
                elif (addr%4 == 2):
                    mem_write_val = lsb2
                else:
                    mem_write_val = lsb3
            else:
                if (addr%4 == 0 or addr%4 == 1):
                    mem_write_val = lsb1*(2**8) + lsb0
                else:
                    mem_write_val = lsb3*(2**8) + lsb2

            assert 1 == dut.ignore_curr_inst.value.integer
            assert 0 == dut.stall_pc.value.integer
            assert 1 == dut.rd_write_control.value.integer
            assert mem_write_val == dut.rd_write_val.value.integer
            assert rd == dut.rd_out.value.integer
            assert 1 == dut.mem_rw_mode.value.integer
            assert 0 == dut.mem_addr.value.integer

        await RisingEdge(dut.i_clk)
        await Timer(0.1,units="ns")

        assert 0 == dut.ignore_curr_inst.value.integer
        assert 0 == dut.stall_pc.value.integer
        assert 0 == dut.rd_write_control.value.integer
        assert 0 == dut.rd_write_val.value.integer
        assert 0 == dut.rd_out.value.integer
        assert 1 == dut.mem_rw_mode.value.integer
        assert 0 == dut.mem_addr.value.integer

        ld_ctrl = random.randrange(0, 6)
        rd = random.randrange(0, 2**5)
        rs1 = random.randrange(0, 2**30)
        imm = random.randrange(0, 2**12)

        dut.rs1_val.value = rs1
        dut.imm.value = imm
        dut.mem_data.value = 0
        dut.rd_in.value = rd
        dut.load_control.value = ld_ctrl
