choose="Hello"

# Compiler
python3 compiler/JackCompiler.py jack_os/$choose/

# VM Translator
python3 translator.py jack_os/$choose/

# Assembler
python3 assembler.py out.asm #> dbg.asm

# Output: out.asm, out.hack
wc -l out.hack

# CPU Emulator
python3 emulator.py out.hack & # Python
n2t_emu/target/debug/n2t_emu out.hack # Rust
