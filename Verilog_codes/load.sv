
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module load(
    input logic i_clk,
    input logic i_rst,
    input logic [31:0] rs1_val,
    input logic [31:0] imm,
    input logic [31:0] mem_data,
    input logic [4:0] rd_in,
    input logic [2:0] load_control,
    output logic stall_pc,
    output logic ignore_curr_inst,
    output logic rd_write_control,
    output logic [4:0] rd_out,
    output logic [31:0] rd_write_val,
    output logic mem_rw_mode,
    output logic [31:0] mem_addr
);

// Edit the code here begin ---------------------------------------------------

    // assign stall_pc = 'b0;
    // assign ignore_curr_inst = 'b0;
    // assign rd_write_control = 'b0;
    // assign rd_out = 'b0;
    // assign rd_write_val = 'b0;
    // assign mem_rw_mode = 'b0;
    // assign mem_addr = 'b0;

   
   logic  ps,ns;
   logic [31:0] add ;
   logic [2:0] temp_load_control;
   logic [4:0] temp_rd_addr; //E
   always @(posedge i_clk or negedge i_rst)

    
 begin
         if (~i_rst) begin
            ps <= 0;
               add <=0;
               temp_load_control<=0;
         end
        else begin
               ps<=ns;
               if(ns==1) begin //E
               add <=rs1_val+imm;
               temp_load_control<=load_control;
               temp_rd_addr <= rd_in;
               end
            //    rd_in<=rd_out;
        end
 end 

    // always_comb
    // begin
    //     if(ps)
    //      ns=0;
    //      else
    //      ns=1;
    // end
    always_comb
    begin
    // case(offset)
    // 2'b00:load_control
        
        if (~ps)
        begin
            if(load_control==`LD_NOP)
            begin
                stall_pc=0;
                ns=0;
            //     case(load_control).
            //    `LB: mem_addr=((rs1+imm)[7:0]);
            //    `LH:mem_addr=(rs1+imm)[15:0];
            //    `LW:mem_addr=(rs1+imm)[31:0];
            //    `LBU:mem_addr=(rs1+imm)[7:0];
            //    `LHU:mem_addr=(rs1+imm)[15:0];
            //     endcase
                mem_addr=0;
                ignore_curr_inst=0;
                rd_out=0;
                rd_write_val=0;
                rd_write_control=0;
                mem_rw_mode=1;
            end
            else
            begin
                ns=1;
               stall_pc=1;
                mem_addr=rs1_val+imm;
                ignore_curr_inst=0;
                rd_out=0;
                rd_write_val=0;
                rd_write_control=0;
                mem_rw_mode=1;
                
            end
        end
        else
        begin
          stall_pc=0;
          ns=0;
                mem_addr=0;
                ignore_curr_inst=1;
                mem_rw_mode=1;
                rd_write_control=1;//E
                rd_out = temp_rd_addr;

                case (temp_load_control)
            `LB, `LBU: begin
                case (add[1:0])
                    2'b00: rd_write_val = (temp_load_control == `LB) ? {{24{mem_data[7]}}, mem_data[7:0]}   : {24'b0, mem_data[7:0]};
                    2'b01: rd_write_val = (temp_load_control == `LB) ? {{24{mem_data[15]}}, mem_data[15:8]} : {24'b0, mem_data[15:8]};
                    2'b10: rd_write_val = (temp_load_control == `LB) ? {{24{mem_data[23]}}, mem_data[23:16]}: {24'b0, mem_data[23:16]};
                    2'b11: rd_write_val = (temp_load_control == `LB) ? {{24{mem_data[31]}}, mem_data[31:24]}: {24'b0, mem_data[31:24]};
                endcase
            end
              `LH, `LHU: begin
                case (add[1])
                    1'b0: rd_write_val = (temp_load_control == `LH)  ? {{16{mem_data[15]}}, mem_data[15:0]} : {16'b0, mem_data[15:0]};           
                    1'b1: rd_write_val = (temp_load_control == `LH)  ? {{16{mem_data[31]}}, mem_data[31:16]} : {16'b0, mem_data[31:16]};
                endcase
            end
            `LW : rd_write_val = mem_data[31:0];
             default : rd_write_val = 32'b0;

        endcase

            

  


        end
    end
    
// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/load.vcd");
        $dumpvars(0, load);
    end
`endif

endmodule
