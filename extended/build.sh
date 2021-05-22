# Compiler
#../tools/JackCompiler.sh jack_os/
python3 ../course/11/JackCompiler/JackCompiler.py jack_os/

# VM Translator
# They don't provide a VM translator
python3 vm_translator.py jack_os/

# Assembler
#../tools/Assembler.sh out.asm && wc -l out.hack
python3 assembler.py out.asm #> dbg.asm

# Output: out.asm, out.hack
#wc -l out.hack

python3 cpu_emulator.py
