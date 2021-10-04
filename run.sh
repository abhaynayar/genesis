# Create and clean build directory
mkdir -p build

# Dummy file system contents
#echo 1337 > disk.img
# Right now we're using zero.ch8

# Compile kernel/ and $target_dir/
python3 compiler/JackCompiler.py kernel/
python3 compiler/JackCompiler.py userland/

# Move VM files to build directory
mv kernel/*.vm build/
mv userland/*.vm build/

# Translate
python3 vm/vm.py build/
python3 assembler/assembler.py build/out.asm

# Emulate (python or cc)
python3 emulator/old.py build/out.hack
#(cd emulator && make) && emulator/a.out build/out.hack
