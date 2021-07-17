python compiler\JackCompiler.py kernel
python compiler\JackCompiler.py userland
python compiler\JackCompiler.py userland/pong

md build
move kernel\*.vm build
move userland\*.vm build
move userland\pong\*.vm build
echo lostatitagain > disk.img

python translator\translator.py build
python assembler\assembler.py build\out.asm
python emulator\python/main.py build\out.hack