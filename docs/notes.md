# Notes
## Intro

To start, I first had to make sure that the entire stack: from the high-level
programming language down to the CPU was available in code and working. Even
after completing the course and passing all the unit tests, my code for the
entire stack wasn't working when I put it all together.

I could have used the toolchain provided by the course developers, but I was
planning to make some architectural changes. Also the course developers don't
provide a VM translator implementaion. So, I decided to reimplement the entire
stack once again, this time in Python.

I recommend you to understand the build pipeline by reading `run.sh`.

## Thoughts on the new RAM and what will be where:

Right now, every program that we store in the RAM will need to have its own
operating system since we lose all information after we assemble. One way to
solve this problem is to assemble it in the emulator.

But, this is not a good thing. The CPU emulator should only process bits.

Yes, the entire operating system has to be written and compiled beforehand of
course. What was I thinking lol. So you just build the operating system and put
it in the large-ass RAM. That's how operating systems work??? Later on we can
start doing more stuff once we have access to external storage and file systems.

## Reduce the size of the ROM code

We can only have 32768 lines of Hack assembly in the ROM. Eventually we wan't to
store stuff in external disks, but until we can do that, we need to optimize the
current OS, compiler, VM translator to use as less space as possible.

## Implement an assembly-level multiple and divide

Implementing this in an emulator is extremely simple. All we need to do is add
another instruction, something like `D=D*A` and then integrate it upwards into
the stack.

## Implement CPU emulator as actual hardware

Currently, we are looking at the instructions and mapping them to the known
instructions in the specification. Eventually, I want the CPU emulator to act
like real hardware. With buses and wires representing the actual CPU.

## Implement drivers for storage systems

ROM size isn't enough if we want to move forward. We need to start connecting
with devices outside. First we will need to make "hardware" changes to the
emulator such that we can talk to storage devices. Another important question
is: do we want to talk to actual storage devices? Or do we make our own
"standard"?  We can perhaps have a single file on the system and store data in
it using our own or some other popular filesystem ported to Jack-lang.

Once we have "hardware" in the emulator to interact with this, we can keep this
memory mapped as well. Or, we can do some more research on how IO-mapped devices
work and implemented those. I would suggest IO-mapped, since at some point we
want to stop using our RAM for this stuff. Maybe we can shift our screen and
keyboard off the RAM later on as well using this. It will allow us to have a
larger/colored screen without hogging all the RAM.

## Optimize clear screen

TBD
