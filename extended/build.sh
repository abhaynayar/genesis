# Choose directory in test/ to run
choose="Hello"

# Compiling Jack OS
python3 compiler/JackCompiler.py jack_os/

# Compiling test code
python3 compiler/JackCompiler.py test/$choose/

# Translating test code (and hardcoded Jack OS)
python3 vm.py test/$choose/

# Assembling test code
python3 asm.py test/$choose/out.asm
wc -l test/$choose/out.hack

# CPU Emulator
#python3 emu.py test/$choose/out.hack
rs_emu/target/release/n2t_emu test/$choose/out.hack
