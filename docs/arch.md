## Architecture

The <a href="https://nand2tetris.org">nand2tetris</a> computer uses 15 bits for
addressing. This means that there is an upper limit of 32768 instructions that
we can load in the ROM at a time. When you try to compile, translate and
assemble a game of Pong, the CPU emulator says: "Program too large"

Some people in the nand2tetris forums have worked on <a
href="http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Links-to-posts-discussing-generated-Assembly-Language-size-td4031627.html">
optimizing</a> the toolchain. The course authors also provided us with a heavily
optimized version of Pong. So, it is evident that with enough effort you can fit
some really cool stuff into the ROM.

However, I wanted to store even larger programs. I especially wanted to start
working on a more sophisticated operating system which would require much more
space than we could optimize for. So I decided to forego the optimization
"challenge" altogether. Perhaps I'll come back to it later. I moved on to just
making the ROM bigger.

We can't simply increase the size of the ROM. We also need to increase the size
addressable by our registers. You can't access more than 32K unique locations
with only 15 bits to spare. So I changed the architecture from 16-bit to 64-bit.
Now, the addressable space for the instruction memory is far more than the 32K I
could get with the 15-bit addressing.

```
2**(16-1) = 32768
2**(64-1) = 9223372036854775808
```

I had to make some fundamental changes to the architecture and so all the
changes in my extension project are incompatible with the original Hack
platform.

The A instructions changed in a very simple manner: earlier, we used to have a
zero at the MSB and the rest of the bits indicated the value to be put into the
A register. The only difference in the 64-bit version is that the size of the
address value has increased from 15 bits to 63 bits. The MSB is still zero.

The C instructions also needed to be 64-bit wide. In order to make them wider, I
have padded them with zeros to the left. The MSB is hardcoded as 1 to
differentiate them from A instructions. New opcodes have been added to support
multiplication and division in the CPU emulator instead of the OS.
