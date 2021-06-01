# Plumbus

After finishing the [nand2tetris](https://github.com/abhaynayar/nand2tetris)
course, I was interested in extending the platform further. That work is called
plumbus.

## Features

- Multiply and divide in CPU.
- No more ROM. Everything is in RAM. (1MB)
- No more 16-bit. It is a 64-bit computer now.

## Compatibility

Keep in mind that these modifications will create changes throughout the entire
stack, including the CPU. The programs compiled through the toolchain in this
repository will not work on the original Hack platform.

## Requirements

Tested on Ubuntu 20.04. For the compilation, translation and assembling of Jack
programs, you will need Python 3. For the CPU emulator, you will need pygame:
`pip3 install -r requirements.txt`

## Building

Execute `./run.sh`.

What it does:
- Compiles the `*.jack` files in kernel/ and user/.
- Translates the compiled VM code to Hack assembly.
- Assembles the Hack assembly code to machine code.
- Runs the machine code on the CPU emulator.

## Future work

- Shell and filesystem.
- Video memory for screen.
- Hardware-based CPU emulator.
- Virtualized operating system.
- Optimized Python CPU emulator.
- Optimized graphics library in OS.
- Cursor and scroll support for text input.
