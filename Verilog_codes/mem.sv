
module mem(
    input logic i_clk,
    input logic i_rst,
    input logic [9:0] in_mem_addr,
    input logic in_mem_re_web,
    input logic [31:0] in_mem_write_data,
    input logic [3:0] in_mem_byte_en,
    output logic [31:0] out_mem_data
);

logic [31:0] memory_reg [0:1023];
logic [31:0] write_data_muxed;

// Edit the code here begin ---------------------------------------------------
// always @ (negedge i_rst)
// begin
    
// end
always @ (posedge i_clk or negedge i_rst)
begin
    out_mem_data<=0;
if (in_mem_re_web)
  begin
    out_mem_data<=memory_reg[in_mem_addr];
  end
else 
   begin 
// always_comb
//  begin
//     if (in_mem_re_web!=0)
//     begin

//     for (int i=0;i<4;i=i+1)
//       begin
//         if (in_mem_byte_en[i])
//        begin
//          memory_reg[in_mem_addr][(i*8)+7:(i*8)]<=in_mem_write_data[(i*8)+7:(i*8)];
//        end
//       end
//  end
    if (in_mem_byte_en[0])
       begin
         memory_reg[in_mem_addr][7:0]<=in_mem_write_data[7:0];
       end
    if (in_mem_byte_en[1])
       begin
         memory_reg[in_mem_addr][15:8]<=in_mem_write_data[15:8];
       end
    if (in_mem_byte_en[2])
       begin
         memory_reg[in_mem_addr][23:16]<=in_mem_write_data[23:16];
       end
    if (in_mem_byte_en[3])
       begin
         memory_reg[in_mem_addr][31:24]<=in_mem_write_data[31:24];
       end
      end
end

    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/mem.vcd");
        $dumpvars(0, mem);
    end
`endif

endmodule
