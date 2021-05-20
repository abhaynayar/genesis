#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <cctype>
#include <bitset>
#include <unordered_map>
#include <vector>
#include <sstream>

/*
 * auxiliary functions
 */

std::string remove_comments(std::string line) {
        size_t found = line.find("//"); 
        line = line.substr(0, found);
        line.erase(std::remove_if(line.begin(), line.end(), 
                    ::isspace), line.end());
        return line;
}

std::string remove_labels(std::string line) {
    // remember that the comments and whitespace have
    // already been removed, so we only need to check the
    // first character of line for "(" and that will be label

    if(line[0] == '(')
        return "";
    return line;
}

bool is_number(const std::string& s) {
    return !s.empty() 
        && s.find_first_not_of("0123456789") == std::string::npos;
}

void populate_maps(std::unordered_map<std::string,std::string> &comp_map,
        std::unordered_map<std::string,std::string> &dest_map,
        std::unordered_map<std::string,std::string> &jump_map) {

    // dest=comp;jump
    // comp is required, rest are optional
    
    // a=0
    comp_map["0"] =   "0101010";
    comp_map["1"] =   "0111111";
    comp_map["-1"] =  "0111010";
    comp_map["D"] =   "0001100";
    comp_map["A"] =   "0110000";
    comp_map["!D"] =  "0001101";
    comp_map["!A"] =  "0110001";
    comp_map["-D"] =  "0001111";
    comp_map["-A"] =  "0110011";
    comp_map["D+1"] = "0011111";
    comp_map["A+1"] = "0110111";
    comp_map["D-1"] = "0001110";
    comp_map["A-1"] = "0110010";
    comp_map["D+A"] = "0000010";
    comp_map["D-A"] = "0010011";
    comp_map["A-D"] = "0000111";
    comp_map["D&A"] = "0000000";
    comp_map["D|A"] = "0010101";

    // a=1
    comp_map["M"] =   "1110000";
    comp_map["!M"] =  "1110001";
    comp_map["-M"] =  "1110011";
    comp_map["M+1"] = "1110111";
    comp_map["M-1"] = "1110010";
    comp_map["D+M"] = "1000010";
    comp_map["D-M"] = "1010011";
    comp_map["M-D"] = "1000111";
    comp_map["D&M"] = "1000000";
    comp_map["D|M"] = "1010101";

    dest_map[""] = "000";
    dest_map["M"] = "001";
    dest_map["D"] = "010";
    dest_map["MD"] = "011";
    dest_map["A"] = "100";
    dest_map["AM"] = "101";
    dest_map["AD"] = "110";
    dest_map["AMD"] = "111";

    jump_map[""] = "000";
    jump_map["JGT"] = "001";
    jump_map["JEQ"] = "010";
    jump_map["JGE"] = "011";
    jump_map["JLT"] = "100";
    jump_map["JNE"] = "101";
    jump_map["JLE"] = "110";
    jump_map["JMP"] = "111";
}

/*
 * generate symbol table and later use it to convert 
 * symbols in A instructions on the fly in asm2machine
 */

void generate_symbol_table(std::vector<std::string> &file_contents, 
        std::unordered_map<std::string,std::string> &symbol_table) {

    // 1. predefined symbols
    symbol_table["R0"] = "0";
    symbol_table["R1"] = "1";
    symbol_table["R2"] = "2";
    symbol_table["R3"] = "3";
    symbol_table["R4"] = "4";
    symbol_table["R5"] = "5";
    symbol_table["R6"] = "6";
    symbol_table["R7"] = "7";
    symbol_table["R8"] = "8";
    symbol_table["R9"] = "9";
    symbol_table["R10"] = "10";
    symbol_table["R11"] = "11";
    symbol_table["R12"] = "12";
    symbol_table["R13"] = "13";
    symbol_table["R14"] = "14";
    symbol_table["R15"] = "15";
    symbol_table["SCREEN"] = "16384";
    symbol_table["KBD"] = "24576";
    symbol_table["SP"] = "0";
    symbol_table["LCL"] = "1";
    symbol_table["ARG"] = "2";
    symbol_table["THIS"] = "3";
    symbol_table["THAT"] = "4";

    // 2. label symbols
    //       - read the file
    //       - whenever encounter (label)
    //       - store <label,ln>

    int line_counter = 0;
    for(std::string line: file_contents) {
        //std::cout << line_counter << "\t" << line << std::endl;
        line = remove_comments(line);
        if(line != "") {

            line_counter++;

            int left = line.find("(");
            int right = line.find_last_of(")");

            std::string label;

            // if a valid label exists
            if(left != std::string::npos && right != std::string::npos) {
                // extract name from brackets
                label = line.substr(left+1, right-left-1);

                // since it's a label, don't count it as a line
                line_counter--;

                // if the label doesn't exist in the symbol table
                // add it to the symbol table with line number
                if(symbol_table.find(label) == symbol_table.end()) {
                    symbol_table[label] = std::to_string(line_counter);
                }

                
            }
        }
    }
    

    // 3. variable symbols
    //       - set counter to 16
    //       - everytime new variable
    //       - store <var,counter++>

    int variable_counter = 16;

    for(std::string line: file_contents) {
        line = remove_comments(line);
        if(line[0] == '@') {
            std::string variable = line.substr(1);

            // if token after "@" is not a number
            // and it is not already in symbol table
            // add it to the symbol table with counter

            if(!is_number(variable) && symbol_table.find(variable)
                    == symbol_table.end()) {
                symbol_table[variable] = std::to_string(variable_counter);
                variable_counter++;
            }
        }
    }

    // display symbol table
    for(auto elem : symbol_table) {
       std::cout << elem.first << "\t" << elem.second << std::endl;
    }
}

/*
 * take symbolic assembly and output machine code to file
 */

std::string assembly_to_machine(std::vector<std::string>
        &file_contents, std::unordered_map<std::string,std::string> 
        &symbol_table) {

    // hashmaps for C instructions
    std::unordered_map<std::string,std::string> comp_map;
    std::unordered_map<std::string,std::string> dest_map;
    std::unordered_map<std::string,std::string> jump_map;

    // fill up the hashmaps for C instructions
    populate_maps(comp_map, dest_map, jump_map);
    std::ostringstream outfile;

    for(std::string line: file_contents) {

        line = remove_comments(line);
        line = remove_labels(line);

        if(line != "") {

            // if it starts with an "@" then A, otherwise C
            if(line[0] == '@') {

                // processing A instructions
                // always starts with a zero
                outfile << "0";

                // check if integer constant or variable symbol

                int address;
                if(is_number(line.substr(1))) {
                    address = stoi(line.substr(1,std::string::npos));
                } else {
                    address = stoi(symbol_table[line.substr(1)]);
                }
                
                outfile << std::bitset<15>(address).to_string();
                outfile << std::endl;

            } else {
                
                // process C instructions here
                outfile << "111";
                
                // find delimiters
                size_t eq = line.find("=");
                size_t sc = line.find(";");
                std::string comp, dest, jump;

                // branching based on "=" and ";"
                if(eq != std::string::npos) {
                    if(sc != std::string::npos) {
                        comp = line.substr(eq+1, sc-eq);
                        dest = line.substr(0,eq);
                        jump = line.substr(sc+1, std::string::npos);
                    } else {
                        comp = line.substr(eq+1, std::string::npos);
                        dest = line.substr(0,eq);
                        jump = "";
                    }
                } else {
                    if(sc != std::string::npos) {
                        comp = line.substr(0, sc);
                        dest = "";
                        jump = line.substr(sc+1, std::string::npos);
                    } else {
                        comp = line;
                        dest = "";
                        jump = "";
                    }
                }

                outfile << comp_map[comp] << dest_map[dest]
                    << jump_map[jump];
                outfile << std::endl;
            }
        }
    }

    return outfile.str();
}

int main(int argc, char** argv) {

    // assumption: input program is error free
    // incorrect number of parameters
    if(argc < 2) return 1;

    std::string arg1 = std::string(argv[1]);

    // assumption: file exists
    std::ifstream infile;
    infile.open(arg1, std::ios::in);

    // read contents of file into a vector of strings
    std::vector<std::string> file_contents;

    // reading input file into a vector of strings
    std::string temp;
    while(getline(infile, temp))
        file_contents.push_back(temp);
    infile.close();

    // symbolic code to generate symbol table
    std::unordered_map<std::string,std::string> symbol_table;
    generate_symbol_table(file_contents, symbol_table);

    // output filename based on input filename (xxx.asm to xxx.hack)
    std::string fname = arg1.substr(0,arg1.find_last_of(".")) + ".hack";
    std::ofstream outfile(fname);
    
    // convert non-symbolic assembly to machine code
    outfile << assembly_to_machine(file_contents, symbol_table);
    outfile.close();
    return 0;
}

