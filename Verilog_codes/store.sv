
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module store(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] rs1_val,
    input logic [31:0] rs2_val,
    input logic [31:0] imm,
    input logic [2:0] store_control,
    output logic stall_pc,
    output logic ignore_curr_inst,
    output logic mem_rw_mode,
    output logic [31:0] mem_addr,
    output logic [31:0] mem_write_data,
    output logic [3:0] mem_byte_en
);

// Edit the code here begin ---------------------------------------------------

    // assign stall_pc = 'b0;
    // assign ignore_curr_inst = 'b0;
    // assign mem_rw_mode = 'b0;
    // assign mem_addr = 'b0;
    // assign mem_write_data = 'b0;
    // assign mem_byte_en = 'b0;
    
always_comb
begin
    if (store_control!=`STR_NOP)
    begin
       stall_pc=1;
       mem_rw_mode=0;
       mem_addr=rs1_val+imm;
        case(store_control)
    
          `SB:begin
            case(mem_addr[1:0])
            2'b00:begin
                mem_byte_en=4'b0001;
            mem_write_data={24'b0,rs2_val[7:0]};
            end
            2'b01:begin
                mem_byte_en=4'b0010;
            mem_write_data={16'b0,rs2_val[7:0],8'b0};
            end
            2'b10:
            begin
                mem_byte_en=4'b0100;
                mem_write_data={8'b0,rs2_val[7:0],16'b0};
            end
            2'b11:begin
                mem_byte_en=4'b1000;
            mem_write_data={rs2_val[7:0],24'b0};
            end
            endcase
          end
          `SH:begin
            case(mem_addr[1])
            1'b0:begin
                mem_byte_en=4'b0011;
                mem_write_data={16'b0,rs2_val[15:0]};
            end
            1'b1:begin
                mem_byte_en=4'b1100;
            mem_write_data={rs2_val[15:0],16'b0};
            end
            endcase
          end
          `SW:begin
                mem_byte_en=4'b1111;
          mem_write_data=rs2_val[31:0];
          end
          default: mem_write_data=0;
    
        endcase
    end
    
    else
    begin
    stall_pc =0;
    mem_rw_mode =1;
    mem_addr =0;
    mem_write_data =0;
    mem_byte_en =0;
    end
end  
 always @ (posedge i_clk or negedge i_rst)
      begin
        if (~i_rst)
        
           ignore_curr_inst<=1'b0;
            
    
        else
        
          ignore_curr_inst<=stall_pc;
          
 
      end 
      
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/store.vcd");
        $dumpvars(0, store);
    end
`endif

endmodule
