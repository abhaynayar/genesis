# Compiling kernel/ and $target_dir/
python3 compiler/JackCompiler.py kernel/
python3 compiler/JackCompiler.py userland/

# Dummy file system contents
echo 1337 > build/disk.img

# Moving VM files to build directory
mkdir -p build
rm build/*
mv kernel/*.vm build/
mv userland/*.vm build/

# Translating
python3 translator/translator.py build/
python3 assembler/assembler.py build/out.asm
python3 emulator/emulator.py build/out.hack