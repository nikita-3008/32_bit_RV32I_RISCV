
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module decode_jump_inst(
    input logic [31:0] instruction_code,
    output logic [4:0] rd,
    output logic [4:0] rs1,
    output logic [20:0] imm,
    output logic [1:0] jump_control
);

// Edit the code here begin ---------------------------------------------------

    assign rd = instruction_code[11:7];
  always_comb
    begin
        case(instruction_code[6:0])
         7'b1101111:begin
                      imm= {instruction_code[31],instruction_code[19:12],instruction_code[20],instruction_code[30:21],1'b0 };
                      rs1=5'b00000;
                      jump_control= `JAL;
         end
         7'b1100111:if(instruction_code[14:12]==3'b000)
                  begin
                     imm= {9'b000000000,instruction_code[31:20]};
                     rs1=instruction_code[19:15];
                     jump_control= `JALR;
                   end
                   else begin
                    imm= 0;
                    rs1=5'b00000;
                    jump_control= `JMP_NOP;
                   end
        default: begin
            imm= 0;
            rs1=5'b00000;
            jump_control= `JMP_NOP;
        end

        endcase
    end
                    


// Edit the code here end -----------------------------------------------------

/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/decode_jump_inst.vcd");
        $dumpvars(0, decode_jump_inst);
    end
`endif

endmodule
