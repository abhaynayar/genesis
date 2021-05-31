# Requirements
mkdir -p build
pip3 install -r requirements.txt

# Compiling kernel and user
python3 compiler/JackCompiler.py kernel/
python3 compiler/JackCompiler.py user/

# Moving VM files to build directory
cp kernel/*.vm build/
cp user/*.vm build/

# Translating
python3 translator.py build/

# Assembling
python3 assembler.py build/out.asm 
wc -l build/out.hack

# Emulating
python3 emulator/py_emu/von.py build/out.hack
