# nand2tetris

This repository aims to extend the [nand2tetris](https://nand2tetris.org)
platform, with a focus on extending the Jack operating system.

## Blog

* **[Introduction](blog/intro.md)**
* **[Architecture](blog/arch.md)**
* **[Memory Layout](blog/memlay.md)**
* **[Boot](blog/boot.md)**
* Interrupts
* Processes

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

## Todo

- ~~Remove docs/.~~
- ~~16-bit to 64-bit.~~
- ~~Everything in RAM.~~
- ~~Multiply and divide in CPU.~~
- CamelCase everywhere?
- Self-hosting compiler.
- Better compiler errors.
- Optimize VM translator.
- VM translator to RISC-V.
- Implement for loop in Jack.
- Hardware-based CPU emulator.
- Optimized Python CPU emulator.
- Provide isolation on CPU level?
- Optimized graphics library in OS.
- Cursor and scroll support for text input.
- Print string and new-line in the same function.
- Output multiple files from assembler; concat them in the build script.
- While updating screen, check if it is already set and then don't update.
