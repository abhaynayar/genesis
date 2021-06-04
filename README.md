# nand2tetris

After finishing the [nand2tetris](https://nand2tetris.org) course, I was
interested in extending the platform further. This repository contains those
extensions.

## Features

- Multiply and divide in CPU.
- No more ROM. Everything is in RAM. (1MB)
- No more 16-bit. It is a 64-bit computer now.

## Compatibility

Keep in mind that these modifications disrupt the entire stack, including the
CPU. The programs compiled through the toolchain in this repository will not
work on the original Hack platform.

## Build

Tested on Ubuntu 20.04.

Get the code:

```
git clone https://github.com/abhaynayar/nand2tetris
cd nand2tetris
```

For the CPU emulator, you need to install pygame.

```
pip3 install pygame
```

For the compilation, translation and assembling of Jack programs, you will need
Python3. You can run the entire system using `run.sh` in the root directory:

```
./run.sh
```

What `run.sh` does:
- Compiles the `*.jack` files in `kernel/` and `user/` directories.
- Copies the VM files to the `build/` directory.
- Translates the compiled VM code to Hack assembly. `build/out.asm`
- Assembles the Hack assembly code to machine code. `build/out.hack`
- Runs the machine code on the CPU emulator.

## Future work

- Shell and filesystem.
- Video memory for screen.
- Hardware-based CPU emulator.
- Virtualized operating system.
- Optimized Python CPU emulator.
- Optimized graphics library in OS.
- Cursor and scroll support for text input.
