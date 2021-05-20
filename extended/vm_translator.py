import os
import sys

def remove_comments(x):
    y = x.find('//')
    return x[:y]

#### ------------------ Error handlers --------------------- ####

def err(x):
    print(x)
    exit()

#### ------------------ Global variables ------------------- ####

label_counter = 1 # LABEL0 is used in bootstrap
module_name = ""

#### ------------------ Bootstrap code --------------------- ####

bootstrap = "// bootstrap code\n"
bootstrap += "@256\n"
bootstrap += "D=A\n"
bootstrap += "@SP\n"
bootstrap += "M=D\n"
bootstrap += "// call Sys.init 0\n"
bootstrap += "@LABEL0\n"
bootstrap += "D=A\n"
bootstrap += "@SP\n"
bootstrap += "A=M\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "M=M+1\n"
bootstrap += "@LCL\n"
bootstrap += "D=M\n"
bootstrap += "@SP\n"
bootstrap += "A=M\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "M=M+1\n"
bootstrap += "@ARG\n"
bootstrap += "D=M\n"
bootstrap += "@SP\n"
bootstrap += "A=M\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "M=M+1\n"
bootstrap += "@THIS\n"
bootstrap += "D=M\n"
bootstrap += "@SP\n"
bootstrap += "A=M\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "M=M+1\n"
bootstrap += "@THAT\n"
bootstrap += "D=M\n"
bootstrap += "@SP\n"
bootstrap += "A=M\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "M=M+1\n"
bootstrap += "@SP\n"
bootstrap += "D=M\n"
bootstrap += "@0\n"
bootstrap += "D=D-A\n"
bootstrap += "@5\n"
bootstrap += "D=D-A\n"
bootstrap += "@ARG\n"
bootstrap += "M=D\n"
bootstrap += "@SP\n"
bootstrap += "D=M\n"
bootstrap += "@LCL\n"
bootstrap += "M=D\n"
bootstrap += "@Sys.init\n"
bootstrap += "0;JMP\n"
bootstrap += "(LABEL0)\n";
bootstrap += "\n\n\n"


#### ----------------- Optimizing return ----------------- ####
# bootstrap += "// return common code\n"
# bootstrap += "($RETURN$)\n"

# # endFrame(R13) = LCL
# bootstrap += "@LCL\n"
# bootstrap += "D=M\n"
# bootstrap += "@R13\n"
# bootstrap += "M=D\n"

# # If no arg, retAddr is overwritten
# # So we have to store it beforehand
# # retAddr(R14) = *(endFrame - 5)
# bootstrap += "@5\n"
# bootstrap += "A=D-A\n"
# bootstrap += "D=M\n"
# bootstrap += "@R14\n"
# bootstrap += "M=D\n"

# # *ARG = pop()
# bootstrap += "@SP\n"
# bootstrap += "M=M-1\n"
# bootstrap += "A=M\n"
# bootstrap += "D=M\n"
# bootstrap += "@ARG\n"
# bootstrap += "A=M\n"
# bootstrap += "M=D\n"

# # SP = ARG+1
# bootstrap += "D=A\n"
# bootstrap += "@SP\n"
# bootstrap += "M=D+1\n"

# # THAT = *(endFrame - 1)
# bootstrap += "@R13\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M\n"
# bootstrap += "@THAT\n"
# bootstrap += "M=D\n"

# # THIS = *(endFrame - 2)
# bootstrap += "@R13\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M\n"
# bootstrap += "@THIS\n"
# bootstrap += "M=D\n"

# # ARG = *(endFrame - 3)
# bootstrap += "@R13\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M\n"
# bootstrap += "@ARG\n"
# bootstrap += "M=D\n"

# # LCL = *(endFrame - 4)
# bootstrap += "@R13\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M\n"
# bootstrap += "@LCL\n"
# bootstrap += "M=D\n"

# # goto retAddr
# bootstrap += "@R14\n"
# bootstrap += "A=M\n"
# bootstrap += "0;JMP\n"
# bootstrap += "\n\n\n"


##### ----------------- Optimizing gt ----------------- ####
# bootstrap += "@SP\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M\n"
# bootstrap += "@SP\n"
# bootstrap += "AM=M-1\n"
# bootstrap += "D=M-D\n"
# bootstrap += "@LABEL" + str(label_counter) + "\n"
# label_counter += 1
# bootstrap += "D;JGT\n"
# bootstrap += "@SP\n"
# bootstrap += "A=M\n"
# bootstrap += "M=0\n"
# bootstrap += "@LABEL" + str(label_counter) + "\n"
# label_counter -= 1
# bootstrap += "0;JMP\n"
# bootstrap += "(LABEL" + str(label_counter) + ")\n"
# label_counter += 1
# bootstrap += "@SP\n"
# bootstrap += "A=M\n"
# bootstrap += "M=-1\n"
# bootstrap += "(LABEL" + str(label_counter) + ")\n"
# label_counter += 1
# bootstrap += "@SP\n"
# bootstrap += "M=M+1\n"


#### ----------------- Mapping functions ------------------- ####

# Map segment-token (from vm-code) to segment-register (in assembly)
def register_name(segment):
    if segment == "local": return "LCL"
    elif segment == "argument": return "ARG"
    elif segment == "this": return "THIS"
    elif segment == "that": return "THAT"
    else: err("Unknown segment " + segment)

#### ------------ Code writers by command types ------------ ####

def c_arithmetic(cmd):
    global label_counter
    out = "// " + cmd + "\n"

    if cmd == "add":
        out += "@SP\n"
        out += "A=M\n"
        out += "A=A-1\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "M=D+M\n"
        out += "@SP\n"
        out += "M=M-1\n"

    elif cmd == "sub":
        out += "@SP\n"
        out += "A=M\n"
        out += "A=A-1\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "M=M-D\n"
        out += "@SP\n"
        out += "M=M-1\n"

    elif cmd == "neg":
        out += "@SP\n"
        out += "A=M\n"
        out += "A=A-1\n"
        out += "M=-M\n"

    elif cmd == "eq":
        out += "@SP\n"
        out += "AM=M-1\n"
        out += "D=M\n"
        out += "@SP\n"
        out += "AM=M-1\n"
        out += "D=M-D\n"
        out += "@LABEL" + str(label_counter) + "\n"
        out += "D;JEQ\n"
        out += "D=1\n"
        out += "(LABEL" + str(label_counter) + ")\n"
        label_counter += 1
        out += "D=D-1\n"
        out += "@SP\n"
        out += "A=M\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M+1\n"
    
    elif cmd == "gt":
        out += "@SP\n"
        out += "M=M-1\n"
        out += "A=M\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "D=M-D\n"
        out += "@LABEL" + str(label_counter) + "\n"
        out += "D;JGT\n"
        out += "@SP\n"
        out += "A=M-1\n"
        out += "M=0\n"
        out += "@LABEL" + str(label_counter+1) + "\n"
        out += "0;JMP\n"
        out += "(LABEL" + str(label_counter) + ")\n"
        out += "@SP\n"
        out += "A=M-1\n"
        out += "M=-1\n"
        out += "(LABEL" + str(label_counter+1) + ")\n"
        label_counter += 2
        
        # My code:
        # out += "@SP\n"
        # out += "AM=M-1\n"
        # out += "D=M\n"
        # out += "@SP\n"
        # out += "AM=M-1\n"
        # out += "D=M-D\n"
        # out += "@LABEL" + str(label_counter) + "\n"
        # label_counter += 1
        # out += "D;JGT\n"
        # out += "@SP\n"
        # out += "A=M\n"
        # out += "M=0\n"
        # out += "@LABEL" + str(label_counter) + "\n"
        # label_counter -= 1
        # out += "0;JMP\n"
        # out += "(LABEL" + str(label_counter) + ")\n"
        # label_counter += 1
        # out += "@SP\n"
        # out += "A=M\n"
        # out += "M=-1\n"
        # out += "(LABEL" + str(label_counter) + ")\n"
        # label_counter += 1
        # out += "@SP\n"
        # out += "M=M+1\n"
        
        # Optimization code:
        # out += "@$RIP123\n"
        # out += "D=A\n"
        # out += "@$GT$\n"
        # out += "0;JMP\n"
    
    elif cmd == "lt":
        out += "@SP\n"
        out += "M=M-1\n"
        out += "A=M\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "D=M-D\n"
        out += "@LABEL" + str(label_counter) + "\n"
        out += "D;JLT\n"
        out += "@SP\n"
        out += "A=M-1\n"
        out += "M=0\n"
        out += "@LABEL" + str(label_counter+1) + "\n"
        out += "0;JMP\n"
        out += "(LABEL" + str(label_counter) + ")\n"
        out += "@SP\n"
        out += "A=M-1\n"
        out += "M=-1\n"
        out += "(LABEL" + str(label_counter+1) + ")\n"
        label_counter += 2

        # out += "@SP\n"
        # out += "AM=M-1\n"
        # out += "D=M\n"
        # out += "@SP\n"
        # out += "AM=M-1\n"
        # out += "D=M-D\n"
        # out += "@LABEL" + str(label_counter) + "\n"
        # out += "D;JLT\n"
        # out += "@SP\n"
        # out += "A=M\n"
        # out += "M=0\n"
        # out += "@LABEL" + str(label_counter+1) + "\n"
        # out += "0;JMP\n"
        # out += "(LABEL" + str(label_counter) + ")\n"
        # out += "@SP\n"
        # out += "A=M\n"
        # out += "M=-1\n"
        # out += "(LABEL" + str(label_counter+1) + ")\n"
        # out += "@SP\n"
        # out += "M=M+1\n"
        # label_counter += 2

    elif cmd == "and":
        out += "@SP\n"
        out += "A=M\n"
        out += "A=A-1\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "M=D&M\n"
        out += "@SP\n"
        out += "M=M-1\n"
    
    elif cmd == "or":
        out += "@SP\n"
        out += "A=M\n"
        out += "A=A-1\n"
        out += "D=M\n"
        out += "A=A-1\n"
        out += "M=D|M\n"
        out += "@SP\n"
        out += "M=M-1\n"
    
    elif cmd == "not":
        out += "@SP\n"
        out += "M=M-1\n"
        out += "A=M\n"
        out += "M=!M\n"
        out += "@SP\n"
        out += "M=M+1\n"

        # My code:
        # out += "@SP\n"
        # out += "A=M\n"
        # out += "A=A-1\n"
        # out += "M=!M\n"

    out += '\n'
    return out

def c_push(cmd, segment, index):
    global module_name
    out = "// push " + segment + " " + index + "\n"

    if segment == "constant":
        out += "@" + index + "\n"
        out += "D=A\n"
        out += "@SP\n"
        out += "A=M\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M+1\n"

    elif segment in ["local", "argument", "this", "that"]:
        out += "@" + index + "\n"
        out += "D=A\n"
        out += "@" + register_name(segment) + "\n"
        out += "A=D+M\n"
        out += "D=M\n"
        out += "@SP\n"
        out += "A=M\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M+1\n"

    elif segment == "temp":
        out += "@" + index + "\n"
        out += "D=A\n"
        out += "@5\n"
        out += "A=D+A\n"
        out += "D=M\n"
        out += "@SP\n"
        out += "A=M\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M+1\n"
        
    #*SP=THIS/THAT, SP++
    elif segment == "pointer":
        if index == "0":
            out += "@THIS\n"
            out += "D=M\n"
            out += "@SP\n"
            out += "A=M\n"
            out += "M=D\n"
            out += "@SP\n"
            out += "M=M+1\n"
    
        elif index == "1":
            out += "@THAT\n"
            out += "D=M\n"
            out += "@SP\n"
            out += "A=M\n"
            out += "M=D\n"
            out += "@SP\n"
            out += "M=M+1\n"
        
        else: err("Invalid index for pointer segment: " + index)
    
    elif segment == "static":
        # "@" + module_name + "." + index
        out += "@" + module_name + "." + index + "\n"
        out += "D=M\n"
        out += "@SP\n"
        out += "A=M\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M+1\n"

    else: err("Invalid segment for push: " + segment)
    out += "\n"
    return out

def c_pop(cmd, segment, index):
    global module_name
    out = "// pop " + segment + " " + index + "\n"

    # Note: can't pop into CONSTANT
    if segment in ["local", "argument", "this", "that"]:

        # We can use R13 as an auxiliary variable:
        # TEMP ends at R12 and STATIC starts at R16
        out += "@" + register_name(segment) + "\n"
        out += "D=M\n"
        out += "@" + index + "\n"
        out += "D=D+A\n"
        out += "@R13\n"
        out += "M=D\n"      # addr = segment + index
        out += "@SP\n"
        out += "M=M-1\n"    # SP--
        out += "A=M\n"
        out += "D=M\n"      # D = *SP
        out += "@R13\n"
        out += "A=M\n"      # A = *(segment+index)
        out += "M=D\n"      # *(segment+index) = *SP

    elif segment == "temp":
        out += "@5\n"
        out += "D=A\n"
        out += "@" + index + "\n"
        out += "D=D+A\n"
        out += "@R13\n"
        out += "M=D\n"
        out += "@SP\n"
        out += "M=M-1\n"
        out += "A=M\n"
        out += "D=M\n"
        out += "@R13\n"
        out += "A=M\n"
        out += "M=D\n"

    # SP--, THIS/THAT=*SP
    elif segment == "pointer":
        if index == "0": #THIS
            out += "@SP\n"
            out += "M=M-1\n"
            out += "A=M\n"
            out += "D=M\n"
            out += "@THIS\n"
            out += "M=D\n"

        elif index == "1": #THAT
            out += "@SP\n"
            out += "M=M-1\n"
            out += "A=M\n"
            out += "D=M\n"
            out += "@THAT\n"
            out += "M=D\n"

        else: err("Invalid index for pointer segment: " + index)


    elif segment == "static":
        # "@" + module_name + "." + index
        out += "@SP\n"
        out += "M=M-1\n"
        out += "A=M\n"
        out += "D=M\n"
        out += "@" + module_name + "." + index + "\n"
        out += "M=D\n"

    else: err("Invalid segment for pop: " + segment)
    out += "\n"
    return out

def c_label(label):
    out = "// label " + label + "\n"
    out += "(" + label + ")\n"
    out += "\n"
    return out

def c_goto(label):
    out = "// goto " + label + "\n"
    out += "@" + label + "\n"
    out += "0;JMP\n";
    out += "\n"
    return out

def c_if(label):
    # We have to pop condition on top of the stack
    # Note: true is -1, false is 0
    out = "// if-goto " + label + "\n"
    out += "@SP\n"
    out += "M=M-1\n"
    out += "A=M\n"
    out += "D=M\n"
    out += "@" + label + "\n"
    out += "D;JNE\n"
    out += "\n"
    return out

def c_function(function_name, num_vars):
    global label_counter

    out = "// function " + function_name + " " + num_vars + "\n"
    out += "(" + function_name + ")\n"
    out += "@" + num_vars + "\n"
    out += "D=A\n"
    out += "(LABEL" + str(label_counter) + ")\n"
    label_counter += 1
    out += "@LABEL" + str(label_counter) + "\n"
    label_counter -= 1
    out += "D;JEQ\n"

    # nArgs times:
    # push constant 0
    out += "@SP\n"
    out += "A=M\n"
    out += "M=0\n"
    out += "@SP\n"
    out += "M=M+1\n"
    out += "D=D-1\n"
    out += "@LABEL" + str(label_counter) + "\n"
    label_counter += 1
    out += "0;JMP\n"
    out += "(LABEL" + str(label_counter) + ")\n";
    label_counter += 1

    out += "\n"
    return out

def c_return():

    # Optimize code:
    # out = "// return\n"
    # out += "@$RETURN$\n"
    # out += "0;JMP\n"
    # out += "\n"
    # return out

    # My code:
    out = "// return\n"

    # endFrame(R13) = LCL
    out += "@LCL\n"
    out += "D=M\n"
    out += "@R13\n"
    out += "M=D\n"

    # If no arg, retAddr is overwritten
    # So we have to store it beforehand
    # retAddr(R14) = *(endFrame - 5)

    # Their code:
    # out += "@R13\n"
    # out += "D=M\n"
    # out += "@5\n"
    # out += "D=D-A\n"
    # out += "A=D\n"
    # out += "D=M\n"
    # out += "@RET\n"
    # out += "M=D\n"

    # My code:
    out += "@5\n"
    out += "A=D-A\n"
    out += "D=M\n"
    out += "@R14\n"
    out += "M=D\n"

    # *ARG = pop()
    out += "@SP\n"
    out += "M=M-1\n"
    out += "A=M\n"
    out += "D=M\n"
    out += "@ARG\n"
    out += "A=M\n"
    out += "M=D\n"

    # SP = ARG+1
    # Their code:
    # out += "@ARG\n"
    # out += "D=M\n"
    # out += "@SP\n"
    # out += "M=D+1\n"

    # My code:
    out += "D=A\n"
    out += "@SP\n"
    out += "M=D+1\n"

    # THAT = *(endFrame - 1)
    out += "@R13\n"
    out += "AM=M-1\n"
    out += "D=M\n"
    out += "@THAT\n"
    out += "M=D\n"

    # THIS = *(endFrame - 2)
    out += "@R13\n"
    out += "AM=M-1\n"
    out += "D=M\n"
    out += "@THIS\n"
    out += "M=D\n"

    # ARG = *(endFrame - 3)
    out += "@R13\n"
    out += "AM=M-1\n"
    out += "D=M\n"
    out += "@ARG\n"
    out += "M=D\n"

    # LCL = *(endFrame - 4)
    out += "@R13\n"
    out += "AM=M-1\n"
    out += "D=M\n"
    out += "@LCL\n"
    out += "M=D\n"

    # goto retAddr
    out += "@R14\n"
    out += "A=M\n"
    out += "0;JMP\n"

    out += "\n"
    return out


def c_call(function_name, num_args):
    global label_counter
    out = "// call " + function_name + " " + num_args + "\n"

    # push retAddr
    out += "@LABEL" + str(label_counter) + "\n"
    out += "D=A\n"
    out += "@SP\n"
    out += "A=M\n"
    out += "M=D\n"
    out += "@SP\n"
    out += "M=M+1\n"

    # push LCL
    out += "@LCL\n"
    out += "D=M\n"
    out += "@SP\n"
    out += "A=M\n"
    out += "M=D\n"
    out += "@SP\n"
    out += "M=M+1\n"

    # push ARG
    out += "@ARG\n"
    out += "D=M\n"
    out += "@SP\n"
    out += "A=M\n"
    out += "M=D\n"
    out += "@SP\n"
    out += "M=M+1\n"

    # push THIS
    out += "@THIS\n"
    out += "D=M\n"
    out += "@SP\n"
    out += "A=M\n"
    out += "M=D\n"
    out += "@SP\n"
    out += "M=M+1\n"

    # push THAT
    out += "@THAT\n"
    out += "D=M\n"
    out += "@SP\n"
    out += "A=M\n"
    out += "M=D\n"
    out += "@SP\n"
    out += "M=M+1\n"

    # ARG = (SP-5)-nArgs
    out += "@SP\n"
    out += "D=M\n"
    out += "@" + num_args + "\n"
    out += "D=D-A\n"
    out += "@5\n"
    out += "D=D-A\n"
    out += "@ARG\n"
    out += "M=D\n"

    # LCL = SP
    out += "@SP\n"
    out += "D=M\n"
    out += "@LCL\n"
    out += "M=D\n"

    # goto function_name
    out += "@" + function_name + "\n"
    out += "0;JMP\n"

    # (retAddr)
    out += "(LABEL" + str(label_counter) + ")\n"
    label_counter += 1

    out += "\n"
    return out

def main():
    if len(sys.argv) != 2:
        err("Usage: python3 vm_translator.py [FILE/DIR]")

    arg1 = sys.argv[1]
    vm_file_paths = []


    if os.path.isdir(arg1) == True: # If it is a directory
        for f in os.listdir(arg1):  # Traverse throught the directory
            if f.endswith(".vm"):   # Add all .vm files to a list
                # Need arg1 and '/' for some relative paths
                vm_file_paths.append(arg1+"/"+f)
    
    elif os.path.isfile(arg1):           # Else if it is a file
        if arg1.endswith(".vm"):         # If it is a .vm file
            vm_file_paths.append(arg1)   # Append it to the list

    if vm_file_paths == []: # Exit if we can't find any .vm files
        err("Invalid input file or directory")

    final_output = open("out.asm", "w")
    final_output.write(bootstrap)

    global module_name # Forgot to add this, caused troubles ;)

    for vm_file_path in vm_file_paths:

        filename_without_extension = vm_file_path[:-3]
        module_name = filename_without_extension.split("/")[-1]
        asm_file_output = filename_without_extension+".asm"
        final_output.write("// ---- " + asm_file_output + " ---- \n")

        vm_file_code = open(vm_file_path).readlines()
        for vm_line in vm_file_code:

            vm_line = remove_comments(vm_line)
            if vm_line == "": continue

            cmd = vm_line.split()[0]
            arg1 = ""
            arg2 = ""

            if len(vm_line.split()) == 3:
                arg1 = vm_line.split()[1]
                arg2 = vm_line.split()[2]
            elif len(vm_line.split()) == 2:
                arg1 = vm_line.split()[1]

            asm_line = ""

            if cmd in ["add","sub","neg","and","or","not","eq","gt","lt"]:
                asm_line = c_arithmetic(cmd)
            elif cmd == "push":     asm_line = c_push(cmd, arg1, arg2)
            elif cmd == "pop":      asm_line = c_pop(cmd, arg1, arg2)
            elif cmd == "label":    asm_line = c_label(arg1)
            elif cmd == "goto":     asm_line = c_goto(arg1)
            elif cmd == "if-goto":  asm_line = c_if(arg1)
            elif cmd == "function": asm_line = c_function(arg1, arg2)
            elif cmd == "return":   asm_line = c_return()
            elif cmd == "call":     asm_line = c_call(arg1, arg2)

            else: err("Command type not found: " + cmd)
            final_output.write(asm_line)
        final_output.write("\n\n\n")

if __name__ == "__main__":
    main()
