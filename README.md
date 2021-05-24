# nand2tetris

Building a modern, general-purpose computer system from the ground up.

https://www.nand2tetris.org/

----

## Extended

After finishing the course, I was interested in extending this platform further.
All the development beyond the course is going on in the `extended/` directory.
You can run the understand the build pipline by reading `build.sh` in the
`extended/` directory. The extended directory also contains a README file which
consists of various plans and approaches being used. At the moment, the
development is ad hoc.

To start, I first had to make sure that the entire stack from the high-level
programming language down to the CPU was available in code and working. The
course developers don't provide a VM translator. For this, I developed the
entire stack including the compiler, VM translator, and the assembler in Python.
We have two CPU emulators: one in Rust, the other in Python. You can choose
either of them to run your programs (see build instructions).

### Compatibility

Keep in mind that these modifications will create changes throughout the entire
stack, including the CPU. The programs compiled through the toolchain in the
extended directory will not work on the original Hack platform. Also, you will
need python3 and pygame (for the emulator).

### Build

Go to the `extended/` directory and run `./build.sh`:

- Compiles the `*.jack` files in the `jack_os/$choose` directory.
- Translates the VM code to Hack assembly.
- Assembles the Hack code to machine language.
- Runs the machine code on the chosen CPU emulator.

Configuring `build.sh`:

- Configure the build script by setting the `$choose` variable. This variable
  decides which directory to be built in the `jack_os` directory. For example
  if the variable is set to "Pong" it will compile all the Jack files in
  `jack_os/Pong`. The OS files need to be included in every such directory.
- We have two CPU emulators. You can also choose between the Rust and the Python
  emulator in `build.sh`. After the compilation, translation and assembling has
  been done, the build script invokes the output file in the CPU emulator.
  Comment the line for the emulator you want to use and uncomment the other one
  in the build script.

### Features

- [ ] von Neumann architecture
- [ ] Video memory for screen
- [ ] External storage
- [ ] File system
- [x] Multiply and divide in the CPU emulator

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
