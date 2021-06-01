# Troubleshooting
## Invalid comp value 0x7f

This can happen if you don't have a return value for a function which is
supposed to have a return value.

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


## Debugging the operating system

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
