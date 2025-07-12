
`ifndef FILE_INCL
    `include "processor_defines.sv"
`endif

module decode_reg_inst(
    input logic [31:7] instruction_code,
    output logic [4:0] rs1,
    output logic [4:0] rs2,
    output logic [4:0] rd,
    output logic [4:0] alu_control
);

// Edit the code here begin ---------------------------------------------------

    // assign rs1 = 'b0;
    // assign rs2 = 'b0;
    // assign rd = 'b0;
    // assign alu_control = 'b0;
    always_comb
    begin
        case(instruction_code[14:12])
        3'b000: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`ADD;
                  end
                else if (instruction_code[31:25]==7'b0100000)
                    begin 
                    alu_control=`SUB;
                  end
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b100: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`XOR;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b110: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`OR;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b111: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`AND;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b001: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`SLL;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b101: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`SRL;
                  end
                else if (instruction_code[31:25]==7'b0100000)
                  begin 
                    alu_control=`SRA;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end 
        3'b010: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`SLT;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end
        3'b011: if(instruction_code[31:25]==7'b0000000)
                  begin 
                    alu_control=`SLTU;
                  end
                
                else
                    begin 
                    alu_control=`ALU_NOP;
                  end
        default: alu_control=`ALU_NOP;
        endcase
    
// Edit the code here end -----------------------------------------------------
    end    

    assign rs1=instruction_code[19:15];
    assign rs2=instruction_code[24:20];
    assign rd=instruction_code[11:7];  
/*
	Following section is necessary for dumping waveforms. This is needed for debug and simulations
*/

`ifndef SUBMODULE_DISABLE_WAVES
    initial begin
        $dumpfile("./sim_build/decode_reg_inst.vcd");
        $dumpvars(0, decode_reg_inst);
    end
`endif

endmodule
