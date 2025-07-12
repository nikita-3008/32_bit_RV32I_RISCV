import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import random


async def start_clock(clk_pin):
    clk_pin.value = 0
    await Timer(5, "ns")
    cocotb.start_soon(Clock(clk_pin, 1, units="ns").start())


async def memory_write(dut, addr, wdata, byten):
    dut.in_mem_addr.value = addr
    dut.in_mem_write_data.value = wdata
    dut.in_mem_byte_en.value = byten
    dut.in_mem_re_web.value = 0
    await RisingEdge(dut.i_clk)
    await Timer(1, "ps")
    dut.in_mem_re_web.value = 1


async def memory_read(dut, addr):
    dut.in_mem_addr.value = addr
    await RisingEdge(dut.i_clk)
    await Timer(1, "ps")
    return dut.out_mem_data.value.integer


@cocotb.test()
async def test_memory_access(dut):
    await start_clock(dut.i_clk)
    dut.i_rst.value= 1
    txns = []
    n_bits = len(dut.in_mem_addr)
    for addr in range(2**n_bits):
        wdata = random.randint(0, 2**32-1)
        txns.append((addr, wdata))
    random.shuffle(txns)

    await RisingEdge(dut.i_clk)
    await Timer(1, "ps")

    for addr, wdata in txns:
        await memory_write(dut, addr, wdata, 0b1111)


    await Timer(20, "ns")
    dut.i_rst.value= 0
    await Timer(20, "ns")
    dut.i_rst.value= 1


    random.shuffle(txns)

    for addr, wdata in txns:
        rdata = await memory_read(dut, addr)
        assert rdata == wdata


@cocotb.test()
async def test_byten(dut):
    await start_clock(dut.i_clk)
    await memory_write(dut, 100, 0x01000000, 0b1000)
    await memory_write(dut, 100, 0x00020000, 0b0100)
    await memory_write(dut, 100, 0x00000300, 0b0010)
    await memory_write(dut, 100, 0x00000004, 0b0001)

    rdata = await memory_read(dut, 100)
    assert rdata == 0x01020304
