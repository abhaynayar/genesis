## Interrupts

Sometimes, we want to interrupt the CPU from whatever it is doing, to do
something else. For example, a timer interrupt, or a keyboard interrupt, or a
divide by zero interrupt.

The CPU needs a set of control registers for interrupts. The kernel writes to
one of these control registers and the CPU reads this register in the next cycle
and realizes it has been interrupted. Then it jumps to some other place to
execute the instructions for that interrupt.

Once we are done executing the interrupt, we need to go back to whatever code we
were executing before.

To support interrupts on the Hack CPU, we will need to make same changes to the
CPU specification. For us, this means that we will be changing the CPU emulator.

We need a register to store the contents of our program counter. Our CPU has a
program counter called `PC`.

Right now, when we hit a key on our keyboard, the value at the address 24576 in
the RAM gets set to the keycode of the key we pressed. In an interrupt-driven
architecture, what will be different?
