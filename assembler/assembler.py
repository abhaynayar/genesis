import os
import sys
#import pprint

def err(x):
    print(x)
    exit()

def remove_comments(line):
    #FIXME: Whitespace may cause issues
    comment = line.find("//")
    return line[:comment]

def remove_labels(line):
    # Comments and have already been removed, so we only need to check for
    # "(" and that will be a line with a label

    if(line.find("(") != -1): return "";
    return line;

def main():
    if len(sys.argv) != 2: err("Usage: python3 assembler.py [FILE]")
    arg1 = sys.argv[1]

    if os.path.isfile(arg1) != True: err("File does not exist")
    if arg1.endswith(".asm") != True: err("Invalid file extension")

    input_file = open(arg1, "r")
    input_code = input_file.readlines()

    ############# Generating Symbolic Code ##############

    # 1. Predefined symbols

    symbol_table = dict()
    symbol_table["R0"] = "0"
    symbol_table["R1"] = "1"
    symbol_table["R2"] = "2"
    symbol_table["R3"] = "3"
    symbol_table["R4"] = "4"
    symbol_table["R5"] = "5"
    symbol_table["R6"] = "6"
    symbol_table["R7"] = "7"
    symbol_table["R8"] = "8"
    symbol_table["R9"] = "9"
    symbol_table["R10"] = "10"
    symbol_table["R11"] = "11"
    symbol_table["R12"] = "12"
    symbol_table["R13"] = "13"
    symbol_table["R14"] = "14"
    symbol_table["R15"] = "15"
    symbol_table["SCREEN"] = "16384"
    symbol_table["KBD"] = "24576"
    symbol_table["SP"] = "0"
    symbol_table["LCL"] = "1"
    symbol_table["ARG"] = "2"
    symbol_table["THIS"] = "3"
    symbol_table["THAT"] = "4"

    # 2. Label symbols
    # - Read the file
    # - Whenever encounter (label)
    # - Store <label,ln>

    line_counter = 0
    for line_with_comments in input_code:
        line = remove_comments(line_with_comments)
        
        if line != "": # If line was a comment, move on
            line_counter += 1

            left = line.find("(")
            right = line.rfind(")")
            
            # Check if it is label
            if left != -1 and right != -1:
                
                # Since it's a label, don't count it as a line
                line_counter -= 1

                # If the label doesn't exist in the symbol table add it to
                # the symbol table with line number
                label = line[left+1:right]
                if label not in symbol_table:
                    symbol_table[label] = str(line_counter)
            #print(line_with_comments.strip()+"\t//" + str(line_counter))
        #else: print(line_with_comments.strip())

    # 3. Variable symbols
    # - Set counter to 16
    # - Everytime new variable
    # - Store <var,counter++>
    
    variable_counter = 16
    for line_with_comments in input_code:
        line = remove_comments(line_with_comments)
        if(line.find("@") != -1):
            variable = line[line.find("@")+1:]

            # If token after "@" is not a number and it is not already in 
            # symbol table, add it to the symbol table with counter
            
            if not variable.isnumeric() and variable not in symbol_table:
                symbol_table[variable] = str(variable_counter)
                variable_counter += 1

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(symbol_table)


    ############# Populating Maps ##############

    comp_map = dict()
    dest_map = dict()
    jump_map = dict()

    # dest=comp;jump
    # comp is required, rest are optional
    
    # a=0
    comp_map["0"] =   "0101010"
    comp_map["1"] =   "0111111"
    comp_map["-1"] =  "0111010"
    comp_map["D"] =   "0001100"
    comp_map["A"] =   "0110000"
    comp_map["!D"] =  "0001101"
    comp_map["!A"] =  "0110001"
    comp_map["-D"] =  "0001111"
    comp_map["-A"] =  "0110011"
    comp_map["D+1"] = "0011111"
    comp_map["A+1"] = "0110111"
    comp_map["D-1"] = "0001110"
    comp_map["A-1"] = "0110010"
    comp_map["D+A"] = "0000010"
    comp_map["D-A"] = "0010011"
    comp_map["A-D"] = "0000111"
    comp_map["D&A"] = "0000000"
    comp_map["D|A"] = "0010101"

    # a=1
    comp_map["M"] =   "1110000"
    comp_map["!M"] =  "1110001"
    comp_map["-M"] =  "1110011"
    comp_map["M+1"] = "1110111"
    comp_map["M-1"] = "1110010"
    comp_map["D+M"] = "1000010"
    comp_map["D-M"] = "1010011"
    comp_map["M-D"] = "1000111"
    comp_map["D&M"] = "1000000"
    comp_map["D|M"] = "1010101"

    #heinz
    comp_map["M*D"] = "1000001"
    comp_map["M/D"] = "1000011"
    comp_map["M^D"] = "1000100"

    dest_map[""] = "000"
    dest_map["M"] = "001"
    dest_map["D"] = "010"
    dest_map["MD"] = "011"
    dest_map["A"] = "100"
    dest_map["AM"] = "101"
    dest_map["AD"] = "110"
    dest_map["AMD"] = "111"

    jump_map[""] = "000"
    jump_map["JGT"] = "001"
    jump_map["JEQ"] = "010"
    jump_map["JGE"] = "011"
    jump_map["JLT"] = "100"
    jump_map["JNE"] = "101"
    jump_map["JLE"] = "110"
    jump_map["JMP"] = "111"

    ############# Symbolic to Machine Code ##############

    out_file = open(sys.argv[1][:-4] + ".hack", "w")

    for line_with_comments in input_code:
        line_with_labels = remove_comments(line_with_comments)
        line = remove_labels(line_with_labels)

        if line != "": # If line was a comment or a label, move on ;)
           
            out_line = ""
            # If it starts with an "@" then it's an A instruction
            if line.find("@") != -1:

                # "A" instructions start with a zero
                out_line += "0"

                # Check if it is an integer constant or variable symbol
                address = -1 # FIXME: Arbritrary initial value
                if line[line.find("@")+1:].isnumeric() != False:
                    address = int(line[line.find("@")+1:])
                else:
                    address = int(symbol_table[line[line.find("@")+1:]])

                out_line += format(address, "063b") #milch
                out_line += "\n"

            # If it's not an A instruction, it's a C instruction
            else:
                out_line += "1" #milch
                out_line += "0"*(64-16-1)
                out_line += "111"

                comp = ""
                dest = ""
                jump = ""
                
                eq = line.find("=")
                sc = line.find(";")
                
                if eq != -1 and sc != -1:
                    comp = line[eq+1:sc-eq]
                    dest = line[:eq]
                    jump = line[sc+1:]

                elif eq != -1 and sc == -1:
                    comp = line[eq+1:]
                    dest = line[:eq]
                    jump = ""

                elif eq == -1 and sc != -1:
                    comp = line[:sc]
                    dest = ""
                    jump = line[sc+1:]

                elif eq == -1 and sc == -1:
                    comp = line
                    dest = ""
                    jump = ""

                else: err("It is impossible to reach this condition")

                out_line += comp_map[comp] + dest_map[dest] + jump_map[jump]
                out_line += "\n"

            out_file.write(out_line)

if __name__ == "__main__":
    main()
