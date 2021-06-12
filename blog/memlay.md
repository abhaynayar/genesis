## Memory Layout

Since we will need to support process at some time, we need to be able to store
the registers and memory (code, data, stack) so that we can get back to it
later. The good thing is, for us the registers are stored in the first few cells
in memory so we can consider the RAM of the older architecture as the virtual
memory for one process.

The process thinks it is physical memory. If we have virtual memory, the process
will still have the same model of the memory in mind. That is: the stack pointer
is at zero, stack is at 256, heap is at 2048, and so on.

The layout of the memory (or single process in the future) is as follows:

```
0       SP      Stack Pointer
1       LCL     Points to the base of current VM function's local segment
2       ARG     Points to the base of current VM function's argument segment
3       THIS    Points to the base of this segment in the heap
4       THAT    Points to the base of that segment in the heap
5       Temp0   Temporary segment register
6       Temp1   Temporary segment register
7       Temp2   Temporary segment register
8       Temp3   Temporary segment register
9       Temp4   Temporary segment register
10      Temp5   Temporary segment register
11      Temp6   Temporary segment register
12      Temp7   Temporary segment register
13      R13     General purpose register 13
14      R14     General purpose register 14
15      R15     General purpose register 15
16      Static variables
256     Stack
2048    Heap
16384   MMIO - Screen
24576   MMIO - Keyboard
```

---

The CPU emulator has now been designed to consider the entire memory as one
contiguous block of memory instead of a ROM and a RAM. This is so that in the
future we can load programs into the memory at runtime and execute them.

Since the two types of memories have been merged, the memory layout has also
changed. This change is temporary and will be considered more, once the
operating system develops further.

```
DATA:     0x0000 to 0x3fff
SCREEN:   0x4000 to 0x5fff
KEYBOARD: 0x6000
RESERVED: 0x6001 to 0x7fff
CODE:     0x8000 to 0xfffff
```

With this layout, we have the ability to increase the CODE section as much as we
want, since it is at the tail end. Now, even without the optimized toolchain, we
can run Pong on the CPU emulator.

[Previous](arch.md)
[Next](boot.md)
