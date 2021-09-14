# Genesis

Retro OS written in Jack (from the [nand2tetris](https://nand2tetris.org) course).

## Build

Tested on Ubuntu 20.04.

Clone the repository.

```
git clone https://github.com/abhaynayar/genesis
```

For the compilation, translation and assembling of Jack programs, you need
[Python](https://www.python.org/downloads/). For the CPU emulator, you will need
[pygame](https://www.pygame.org/).

Build and run the project using:

```
./run.sh
```

What the build script does:
- Compiles the `*.jack` files in `kernel/` and `userland/` directories.
- Copies the VM files to the `build/` directory.
- Translates the compiled VM code to Hack assembly. `build/out.asm`
- Assembles the Hack assembly code to machine code. `build/out.hack`
- Runs the machine code on the CPU emulator.

## Docs

* **[Introduction](docs/introduction.md)**
* **[Architecture](docs/architecture.md)**
* **[Memory Layout](docs/memory-layout.md)**
* **[Interrupts](docs/interrupts.md)**

## Todo
Applications

- [ ] Text Editor
	- Hold key for multi-input.
	- SHIFT key support.
	- Backspace support.
- [ ] Chip8 Interpreter
- [ ] GUI Toolkit

Language

- [ ] Hex numbers
- [x] XOR operations
- [ ] Code coverage
- [ ] Error handling
- [ ] Shift operations
- [ ] Inline assembly
- [ ] Coding style guide

System

- [x] C++ Emulator
- [ ] File System
- [ ] Sound Support
- [ ] Timer Interrupts
- [ ] Network Stack
- [ ] Keyboard Interrupts
- [x] Hardware-based CPU emulator

Misc.

- [ ] Fonts with transparent backgrounds.
- [ ] Terminate compiler and batch script on error.
- [ ] Check if Hack file is 64-bit before emulating.
- [ ] Print string and newline in the same function.
- [ ] Check if pixel is already set, if yes then don't update.
- [ ] Implement special keyboard input. (backspace, control, etc.)
- [ ] Output multiple files from assembler; concat them in the build script.
