# nand2tetris

Building a modern, general-purpose computer system from the ground up.

https://www.nand2tetris.org/

----

## Extended

After finishing the course, I was interested in extending this platform further.
All the development beyond the course is going on in the `extended/` directory.
You can understand the build pipline by reading `build.sh` in the `extended/`
directory. The extended directory also contains a README file which consists of
various plans and approaches being used. At the moment, the development is ad
hoc.

To start, I first had to make sure that the entire stack: from the high-level
programming language down to the CPU was available in code and working. The
course developers don't provide a VM translator. For this, I developed the
entire stack including the compiler, VM translator, and the assembler in Python.

### Features

- Multiply and divide in CPU

### To be implemented

- Optimize graphics library in OS
- von Neumann architecture
- Video memory for screen
- External storage
- File system

### Compatibility

Keep in mind that these modifications will create changes throughout the entire
stack, including the CPU. The programs compiled through the toolchain in the
extended directory will not work on the original Hack platform.

### Requirements

Tested on Ubuntu 20.04. For the compilation, translation and assembling of Jack
programs, you will need python3.

We have three CPU emulators in the `extended/emulators` directory. Each of them
has different requirements. I am currently using the Rust-based CPU emulator for
which you will need to [install Rust](https://www.rust-lang.org/tools/install).

### Build

Go to the `extended/` directory.

#### Configuring `build.sh`

Configure the build script by setting the `$choose` variable. This variable
decides which directory is to be built in the `test` directory. For example if
the variable is set to "Pong" it will compile all the Jack files in `test/Pong`.
By default it will run the "Hello" program which prints a string on the screen.

The code to choose the CPU emulator is given in the build script. Just uncomment
the line for the emulator you want to use (at the end of the script). I
recommend using the Rust emulator:

- Rust emulator: build by running `$ cargo build --release` in the
  `emulators/rs_emu` directory. You will need SDL for this and C++.
- C++ emulator: build by running `$ make` in the `emulators/cc_emu` directory.
- Python emulator: configure build script to use `emulators/emu.py`.

#### Running `./build.sh`

- Compiles the `*.jack` files in the `jack_os/$choose` directory.
- Translates the VM code to Hack assembly.
- Assembles the Hack code to machine code.
- Runs the machine code on the chosen CPU emulator.

----

## Course

My work for the course can be found in the `projects/` directory.
The directories have been organized by weeks. Summary below:

<table>
<tr>
<th>Project</th>
<th>Description</th>
</tr>

<tr>
<td>00</td>
<td>Sanity check</td>
</tr>

<tr>
<td>01</td>
<td>Boolean Logic</td>
</tr>

<tr>
<td>02</td>
<td>Boolean Arithmetic</td>
</tr>

<tr>
<td>03</td>
<td>Sequential Logic</td>
</tr>

<tr>
<td>04</td>
<td>Machine Language</td>
</tr>

<tr>
<td>05</td>
<td>Computer Architecture </td>
</tr>

<tr>
<td>06</td>
<td>Assembler</td>
</tr>

<tr>
<td>07</td>
<td>Virtual Machine - Stack Arithmetic</td>
</tr>

<tr>
<td>08</td>
<td>Virtual Machine - Program Control</td>
</tr>

<tr>
<td>09</td>
<td>High-Level Language Project</td>
</tr>

<tr>
<td>10</td>
<td>Compiler - Syntax Analysis</td>
</tr>

<tr>
<td>11</td>
<td>Compiler - Code Generation</td>
</tr>

<tr>
<td>12</td>
<td>Operating System</td>
</tr>
