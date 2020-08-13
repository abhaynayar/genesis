#include <fstream>
#include <iostream>

#include "Enum.h"
#include "CodeWriter.h"

CodeWriter::CodeWriter(std::string filename) {
    // create output file xxx.vm for xxx.asm
    int period = filename.find_last_of(".");
    outfile.open(filename.substr(0,period) + ".asm");

    // init variables
    labelCounter = 0;
}

void CodeWriter::writeArithmetic(std::string cmd) {
    // write vm code as a comment
    outfile << "// " << cmd << std::endl;
    if(cmd == "add") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "M=M+D\n"
                   "@SP\n"
                   "M=M-1\n";
    
    } else if(cmd == "sub") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "M=M-D\n"
                   "@SP\n"
                   "M=M-1\n";
    
    } else if(cmd == "neg") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "M=-M\n";
    
    } else if(cmd == "eq") {
        outfile << "@SP\n"
                   "AM=M-1\n"
                   "D=M\n"
                   "@SP\n"
                   "AM=M-1\n"
                   "D=M-D\n"
                   "@LABEL" << labelCounter << "\n"
                   "D;JEQ\n"
                   "D=1\n"
                   "(LABEL" << labelCounter++ << ")\n"
                   "D=D-1\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n";

    } else if(cmd == "gt") {
        outfile << "@SP\n"
                   "AM=M-1\n"
                   "D=M\n"
                   "@SP\n"
                   "AM=M-1\n"
                   "D=M-D\n"
                   "@LABEL" << labelCounter++ << "\n"
                   "D;JGT\n"
                   "@SP\n"
                   "A=M\n"
                   "M=0\n"
                   "@LABEL" << labelCounter-- << "\n"
                   "0;JMP\n"
                   "(LABEL" << labelCounter++ << ")\n"
                   "@SP\n"
                   "A=M\n"
                   "M=-1\n"
                   "(LABEL" << labelCounter++ << ")\n"
                   "@SP\n"
                   "M=M+1\n";

    } else if(cmd == "lt") {
        outfile << "@SP\n"
                   "AM=M-1\n"
                   "D=M\n"
                   "@SP\n"
                   "AM=M-1\n"
                   "D=M-D\n"
                   "@LABEL" << labelCounter++ << "\n"
                   "D;JLT\n"
                   "@SP\n"
                   "A=M\n"
                   "M=0\n"
                   "@LABEL" << labelCounter-- << "\n"
                   "0;JMP\n"
                   "(LABEL" << labelCounter++ << ")\n"
                   "@SP\n"
                   "A=M\n"
                   "M=-1\n"
                   "(LABEL" << labelCounter++ << ")\n"
                   "@SP\n"
                   "M=M+1\n";
    
    } else if(cmd == "and") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "M=D&M\n"
                   "@SP\n"
                   "M=M-1\n";
    
    } else if(cmd == "or") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "D=M\n"
                   "A=A-1\n"
                   "M=D|M\n"
                   "@SP\n"
                   "M=M-1\n";
    
    } else if(cmd == "not") {
        outfile << "@SP\n"
                   "A=M\n"
                   "A=A-1\n"
                   "M=!M\n";
    }

    outfile << std::endl;
}

void CodeWriter::writePushPop(int cmd, std::string segment, int index) {
    if(cmd == C_PUSH) {
        // write vm code as a comment
        outfile << "// push " << segment << " "
            << index << std::endl;
        
        if(segment == "constant") {
            outfile << "@" << index << "\n"
                    << "D=A\n"
                    << "@SP\n"
                    << "A=M\n"
                    << "M=D\n"
                    << "@SP\n"
                    << "M=M+1\n";
        }
    }

    outfile << std::endl;
}

CodeWriter::~CodeWriter() {
    outfile.close();
}

