# Extending the platfrom

## Optimize clear screen

TBD

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

----

# Rough notes
## VM translator didn't work because of incorrect labels

I'm just going to put this out here because this thing took me about three days
to resolve. I was making globally unique labels. Because of this, my code was
passing all the tests on the course. Since they were unit tests.

As soon as I started to go down the whole stack on my own, I started getting
some hard to find bug in the VM emulator. It took me a long time to first
isolate the bug. When I used my own compiler, with my own OS and their VM
translator, and the test program worked, I knew something was wrong with the VM
translator.

I spent the last few days devising weird techniques for debugging this 
godforsaken low-level nightmare. Some of them I have written below. At this
level, you have to be creative, since you can't just `print("HERE!!!!" + x)`.

Ultimately I figured that the bug was in the implementation of `if-goto` in the
VM translator. I had already been suspicious about that before, but I checked
the implementation. It was simple, and I saw other's people code online and it
seemed that there was nothing wrong.

Finally, today, I was going through the VM code and I pin-pointed exactly the
place where the program went to shit using one of my "creative" debugging
methods below. As I was expecting the VM code, I realized that the same label
was being used multiple times.

I went back to the course and realized that I had missed a crucial part in the
implementation of the VM translator, which was that the labels used in if-goto,
label and goto need to have the module name as a prefix. The compiler provides
you with a numbered suffix for the label, but that suffix is only unique within
the given function. To make it globally unique, you need to prefix it with the
function name.

This was not a "bug", it was just negligence on my part while implementing the
specification. But I still wanted to write about this as this was a fun journey
where the answer was stupid. This happens often and it's always fun.


Debugging the operating system:

```
/////
do Memory.poke(weirdVariable);
do Sys.wait(32767);
/////
```

Debugging the VM translator:

```
/////
@0
A=A-1
D=M
/////
```

## Bootstrap code

So, when I first made my VM translator, I just got the bootstrap code off from
somewhere on the internet. I was in a hurry to finish the course and couldn't be
bothered write it on my own.

Now I realized that I could have just written a simple `call Sys.init` which I
could have then sent through the VM translator. Once that was done, writing the
code to set SP=256 in assembly was trivial, and could be prepended to the
bootstrap code.
