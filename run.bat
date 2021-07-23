python compiler\JackCompiler.py kernel
python compiler\JackCompiler.py userland

md build
move kernel\*.vm build
move userland\*.vm build
echo 1337 > build\disk.img

python translator\translator.py build
python assembler\assembler.py build\out.asm
python emulator\emulator.py build\out.hack