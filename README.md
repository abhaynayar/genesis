# nand2tetris

## About

Building a modern, general-purpose computer system from the ground up.

https://www.nand2tetris.org/

----

## Extended

After finishing the course, I was interested in extending this platform further.

To start, I first had to make sure that the entire stack: from the high-level
programming language down to the CPU was available in code and working. Even
after completing the course and passing all the unit tests, my code for the
entire stack wasn't working when I put it all together.

I could have used the toolchain provided by the course developers, but I was
planning to make some architectural changes. Also the course developers don't
provide a VM translator implementaion. So, I decided to reimplement the entire
stack once again, this time in Python.

I recommend you to understand the build pipeline by reading `run.sh`.

### Compatibility

Keep in mind that these modifications will create changes throughout the entire
stack, including the CPU. The programs compiled through the toolchain in this
repository will not work on the original Hack platform.

### Requirements

Tested on Ubuntu 20.04. For the compilation, translation and assembling of Jack
programs, you will need Python 3. For the CPU emulator, you will need pygame.

### Building

Execute `./run.sh`:

- Compiles the `*.jack` files in the kernel and userspace.
- Translates the compiled VM code to Hack assembly.
- Assembles the Hack assembly code to machine code.
- Runs the machine code on the CPU emulator.

### Features

- Multiply and divide in CPU.
- No more ROM. Everything is in RAM.

### Future work

- xv6-like operating system.
- Optimize graphics library in OS.
- Optimize Python CPU emulator.
- Video memory for screen.

----

## Projects

The coursework is in the `projects/` directory and has been organized by weeks.
Summary below:

<table>

<tr>
<th>Project</th>
<th>Description</th>
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

</table>
