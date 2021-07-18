# Jack OSX

An extension of the Jack operating system (from the
[nand2tetris](https://nand2tetris.org) course).

## About

At first, the goal of this project was to learn about other operating
systems by trying to reimplement well-known features to this operating
system. But, at the moment, the direction being taken is ad hoc. This means
that the operating system will not resemble conventional operating systems.
Instead it will grow on the basis of need.

The downside to this approach is that there will be issues that crop up due
to the lack of foresight. However, this approach will allow for a more
organic approach, without getting bogged down by too many "best practices".
Any contributions that allow for Jack OSX to follow a better and well
thought out plan are welcome.

## Build

You can build the project on Windows and Ubuntu.

For the compilation, translation and assembling of Jack programs, you
need [Python](https://www.python.org/downloads/).

For the CPU emulator, you need pygame.

```
pip3 install pygame
```

Build and run the project using `run.bat` (Windows) or `run.sh` (Ubuntu).

What the build script does:
- Compiles the `*.jack` files in `kernel/` and `userland/` directories.
- Copies the VM files to the `build/` directory.
- Translates the compiled VM code to Hack assembly. `build/out.asm`
- Assembles the Hack assembly code to machine code. `build/out.hack`
- Runs the machine code on the CPU emulator.

## Docs

* **[Introduction](docs/intro.md)**
* **[Architecture](docs/arch.md)**
* **[Memory Layout](docs/memlay.md)**
* **[File System](docs/fs.md)**

## Todo

- [ ] File System
- [ ] Text Editor
- [ ] Command Shell
- [ ] Graphics Editor
- [ ] Network Access
- [ ] Web Browser