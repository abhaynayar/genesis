## Boot

We will need a very small portion of ROM that will contain the boot loader.
But, beyond that, programs that we compile will not run on the ROM as in the
original Hack computer implementation.

The boot loader loads the Jack kernel into the RAM at physical address `idkyet`.
At this point, we don't have virtual memory. We jump to the main method in the
Jack OS. Here we do some privileged stuff and then we jump into unprivileged
mode.

We launch the first `Process` in Main called `UserInit`.
