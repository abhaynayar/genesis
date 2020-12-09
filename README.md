# nand2tetris

Building a general purpose computer from scratch.

https://www.nand2tetris.org/

## Part 1

### Week 1: Logic gates, multiplexors, demultiplexors

- Designed `.hdl` files can be found under `projects/01`
- `.tst` files were scripts that could be run in `tools/CPUEmulator.sh`
- `.cmp` files were supposed to match with our output in `.out` files.

### Week 2: Adders, ALU

- Designed `.hdl` files can be found in `projects/02`
- `ALU-nostat` could be used to check an intermediate state of the ALU.
- `.tst` files were scripts that could be run in `tools/CPUEmulator.sh`
- `.cmp` files were supposed to match with our output in `.out` files.

### Week 3: Bits, Registers, RAM

- `projects/03/a` contains a bit (flip-flop), a register (several bits), a program counter (special register) and RAM (several registers).
- `projects/03/b` contains RAM chips of increasing sizes and it is in a separate folder because apparently our own RAM implementation is slow and we want to reference the built-in version instead of our own.
- Each folder also contains respective testing files.

### Week 4: Programming in Assembly

- `projects/04/fill` contains a program that I wrote in assembly that fills the screen with colour (monochrome) if any key is pressed.
- `projects/04/mult` contains a program that I wrote in assembly to multiply two numbers in the RAM and store the result back in the RAM.
- Each folder also contains respective testing files.

### Week 5: Computer organization

`N/A`

### Week 6: Assembler

- In this week, we build an assembler that takes in an `.asm` file and outputs a `.hack` file containing ASCII 1's and 0's that represent opcodes of the Hack language that can be run on the designed CPU.
- The assembler has been built using C++ and can be found in `projects/06/assembler.cpp`
- To run the assember, first compile it using `g++ -o assembler assembler.cpp` and then `./assembler prog.asm`

## Part 2

### Week 7: Virtual Machine Translator (stack arithmetic)

- In this week we build a VM translator that converts our VM code into Hack assembly language. For now we only build stack arithmetic functionality.
- The program was built in C++ and can be found under `projects/07/VMTranslator` using the supplied makefile.
- This can be tested using programs under `projects/07`

### Week 8: Virtual Machine Translator (program control)

- We finish the VM translator with support for control flow.
- The program can be found under `projects/08/VMTranslator` and can be compiled using the supplied makefile by running `make`
- This can be tested using programs under `projects/08`

### Week 9: Project in higher-level language

- In this week we get familiar with the high-level programming language called Jack by creating our own program in it (for a peer-graded assignment).
- My project was a basic Tic-tac-toe game that can be found under `projects/09/TicTacToe`

### Week 10: Compiler (syntax analysis)

- In this week we start building a compiler by first parsing and tokenizing the input source program in Jack.
- For this project, I chose python3 as my language of choice: `projects/10/JackCompiler`

### Week 11: Compiler (code generation)

- In this week we finish building the compiler by generating code using the tokenized input from the previous project.
- The project has been written in python3 and can be found under `projects/10/JackCompiler`

### Week 12: Operating System

- In this week we implement eight operating system classes to finish our general purpose computer.
- These classes are: Keyboard, Memory, Screen, Output, Sys, Math, Array, String.
- For now, I have just implemented a simple solution for the Memory class because I wasn't able to get the actual heap to work, but you can find the incomplete code in the comments.

