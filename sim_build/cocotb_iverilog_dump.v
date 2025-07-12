module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/load.fst");
    $dumpvars(0, load);
end
endmodule
