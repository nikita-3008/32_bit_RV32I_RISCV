
// OPCODES
`define OP_REG 7'b011_0011
`define OP_IMM 7'b001_0011
`define OP_LOAD 7'b000_0011
`define OP_STORE  7'b010_0011
`define OP_BRANCH 7'b110_0011
`define OP_JAL 7'b110_1111
`define OP_JALR 7'b110_0111
`define OP_LUI 7'b011_0111
`define OP_AUIPC 7'b001_0111

// ALU Operations
`define ALU_NOP 5'd0
`define ADD 5'd1
`define SUB 5'd2
`define XOR 5'd3
`define OR 5'd4
`define AND 5'd5
`define SLL 5'd6
`define SRL 5'd7
`define SRA 5'd8
`define SLT 5'd9
`define SLTU 5'd10
`define ADDI 5'd16
`define XORI 5'd17
`define ORI 5'd18
`define ANDI 5'd19
`define SLLI 5'd20
`define SRLI 5'd21
`define SRAI 5'd22
`define SLTI 5'd23
`define SLTIU 5'd24
`define LUI 5'd28
`define AUIPC 5'd29

// BRANCH Operations
`define BR_NOP 3'd0
`define BEQ 3'd1
`define BNE 3'd2
`define BLT 3'd3
`define BGE 3'd4
`define BLTU 3'd5
`define BGEU 3'd6

// JUMP Operations
`define JMP_NOP 2'd0
`define JAL 2'd1
`define JALR 2'd2

// LOAD Operations
`define LD_NOP 3'd0
`define LB 3'd1
`define LH 3'd2
`define LW 3'd3
`define LBU 3'd4
`define LHU 3'd5

// STORE Operations
`define STR_NOP 3'd0
`define SB 3'd1
`define SH 3'd2
`define SW 3'd3

// LOAD - STATE MACHINES
`define LOAD_RESET 1'b0
`define READ_MEM 1'b1

// STORE - STATE MACHINES
`define STORE_RESET 1'b0
`define WRITE_MEM 1'b1

// MEM Addr Width
`define MEM_ADDR_WD 10

// FILE Included
`define FILE_INCL 1
