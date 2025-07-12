import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import random

@cocotb.test()
async def test_decode_imm_inst(dut):
    cnt = 100

    """ TESTCASE """
    for n in range(cnt):

        inst_addr        = random.randrange(0, 2**32)
        stall_pc         = random.choice([0, 1])
        mem_addr         = random.randrange(0, 2**32)
        mem_rw_mode      = random.choice([0, 1])
        mem_write_data   = random.randrange(0, 2**32)
        mem_byte_en      = random.randrange(0, 2**4)
        ignore_curr_inst = random.choice([0, 1])
        from_mem_data    = random.randrange(0, 2**32)

        dut.inst_addr.value        = inst_addr
        dut.stall_pc.value         = stall_pc
        dut.mem_addr.value         = mem_addr
        dut.mem_rw_mode.value      = mem_rw_mode
        dut.mem_write_data.value   = mem_write_data
        dut.mem_byte_en.value      = mem_byte_en
        dut.ignore_curr_inst.value = ignore_curr_inst
        dut.from_mem_data.value    = from_mem_data


        await Timer(1,units="ns")

        if stall_pc:
            assert mem_addr == dut.to_mem_addr.value.integer
            assert mem_write_data == dut.to_mem_write_data.value.integer
            assert mem_rw_mode == dut.to_mem_rw_mode.value.integer
            assert mem_byte_en == dut.to_mem_byte_en.value.integer
        else:
            assert inst_addr == dut.to_mem_addr.value.integer
            assert 0 == dut.to_mem_write_data.value.integer
            assert 1 == dut.to_mem_rw_mode.value.integer
            assert 0 == dut.to_mem_byte_en.value.integer

        if ignore_curr_inst:
            assert 0 == dut.instruction_code.value.integer
            assert from_mem_data == dut.mem_read_data.value.integer
        else:
            assert from_mem_data == dut.instruction_code.value.integer
            assert 0 == dut.mem_read_data.value.integer
