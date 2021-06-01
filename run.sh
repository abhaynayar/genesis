user="user"

# Compiling kernel and user
python3 compiler/JackCompiler.py kernel/
python3 compiler/JackCompiler.py $user/

# Moving VM files to build directory
mkdir -p build
rm build/*
cp kernel/*.vm build/
cp $user/*.vm build/

# Translating
python3 translator.py build/

# Assembling
python3 assembler.py build/out.asm > build/out.dbg

# Emulating
python3 -m cProfile -s time emulator.py build/out.hack > build/profile.dbg
