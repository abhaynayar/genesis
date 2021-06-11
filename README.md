# nand2tetris

This repository aims to extend the [nand2tetris](https://nand2tetris.org)
platform, with a focus on extending the Jack operating system.

Keep in mind that the modifications disrupt the entire stack, including the CPU.
The programs compiled through the toolchain in this repository will not work on
the original Hack platform. The progress can be found in the blog given below.

## Blog
* **[Introduction](blog/intro.md)**
* **Interrupts**

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
- Compiles the `*.jack` files in `kernel/` and `userland/` directories.
- Copies the VM files to the `build/` directory.
- Translates the compiled VM code to Hack assembly. `build/out.asm`
- Assembles the Hack assembly code to machine code. `build/out.hack`
- Runs the machine code on the CPU emulator.

---

## Future work
- Interrupts.
- Privilege modes.
- System calls.
- Paging.
- Shell.
- Filesystem.
- Video memory.

## Todo
- Hardware-based CPU emulator.
- Optimized Python CPU emulator.
- Optimized graphics library in OS.
- Cursor and scroll support for text input.
- Output multiple files from assembler; concat them in the build script.
- While updating screen, check if it is already set and then don't update.

## Done
- Multiply and divide in CPU.
- No more ROM. Everything is in RAM. (1MB)
- No more 16-bit. It is a 64-bit computer now.
