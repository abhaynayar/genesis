#include <fstream>
#include <iostream>
#include "Enum.h"
#include "CodeWriter.h"

CodeWriter::CodeWriter(std::string filename) {

    // create output file xxx.vm for xxx.asm
    int period = filename.find_last_of(".");
    fnNoExt = filename.substr(0,period);
    outfile.open(fnNoExt + ".asm");

    // fix static variables for files which are in directories
    int last_slash = fnNoExt.find_last_of("/");
    fnNoExt = fnNoExt.substr(last_slash+1);

    // init variables
    labelCounter = 0;
}

CodeWriter::~CodeWriter() {
    outfile.close();
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
        
        // writing vm code as a comment
        outfile << "// push " << segment << " " << index << std::endl;
        
        if(segment == "constant") {
            outfile << "@" << index << "\n"
                       "D=A\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n";
        
        } else if(segment == "local" || segment == "argument" 
                     || segment == "this" || segment == "that") {

            outfile << "@" << index << "\n"
                       "D=A\n"
                       "@" << registerName(segment) << "\n"
                       "A=D+M\n"
                       "D=M\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n";
        
        } else if(segment == "temp") {
            outfile << "@" << index << "\n"
                       "D=A\n"
                       "@5\n"
                       "A=D+A\n"
                       "D=M\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n";
        
        // *SP=THIS/THAT, SP++
        } else if(segment == "pointer") {
            if(index == 0) {  // THIS

                outfile << "@THIS\n"
                           "D=M\n"
                           "@SP\n"
                           "A=M\n"
                           "M=D\n"
                           "@SP\n"
                           "M=M+1\n";

            } else if (index == 1) {  // THAT

                outfile << "@THAT\n"
                           "D=M\n"
                           "@SP\n"
                           "A=M\n"
                           "M=D\n"
                           "@SP\n"
                           "M=M+1\n";
            }
        
        } else if(segment == "static") {

            // "@" + fnNoExt + "." + index
            outfile << "@" << fnNoExt << "." << index << "\n"
                       "D=M\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n";
        }
    
    } else if(cmd == C_POP) {
        
        // NOTE: can't pop into CONSTANT
        // writing vm code as a comment
        
        outfile << "// pop " << segment << " " << index << std::endl;
        if(segment == "local" || segment == "argument"
              || segment == "this" || segment == "that") {

            // we can use R13 as an auxiliary variable:
            // TEMP ends at R12 and STATIC starts at R16
            outfile << "@" << registerName(segment) << "\n"
                       "D=M\n"
                       "@" << index << "\n"
                       "D=D+A\n"
                       "@R13\n"
                       "M=D\n"  // addr = segment + index
                       "@SP\n"
                       "M=M-1\n"  // SP--
                       "A=M\n"
                       "D=M\n"  // D = *SP
                       "@R13\n"
                       "A=M\n"  // A = *(segment+index)
                       "M=D\n";  // *(segment+index) = *SP
        
        } else if(segment == "temp") {

            outfile << "@5\n"
                       "D=A\n"
                       "@" << index << "\n"
                       "D=D+A\n"
                       "@R13\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M-1\n"
                       "A=M\n"
                       "D=M\n"
                       "@R13\n"
                       "A=M\n"
                       "M=D\n";
        
        // SP--, THIS/THAT=*SP
        } else if(segment == "pointer") {
            if(index == 0) {  // THIS
                outfile << "@SP\n"
                           "M=M-1\n"
                           "A=M\n"
                           "D=M\n"
                           "@THIS\n"
                           "M=D\n";

            } else if (index == 1) {  // THAT

                outfile << "@SP\n"
                           "M=M-1\n"
                           "A=M\n"
                           "D=M\n"
                           "@THAT\n"
                           "M=D\n";
            }
        
        } else if(segment == "static") {

            // "@" + fnNoExt + "." + index
            outfile << "@SP\n"
                       "M=M-1\n"
                       "A=M\n"
                       "D=M\n"
                       "@" << fnNoExt << "." << index << "\n"
                       "M=D\n";
        }
 
    }
    
    outfile << std::endl;
}

std::string CodeWriter::registerName(std::string segment) {
    
    // local, argument, this, that, temp
    // @LCL, @ARG, @THIS, @THAT, @5
    
    if(segment == "local") {
        return "LCL";
    } else if(segment == "argument") {
        return "ARG";
    } else if(segment == "this") {
        return "THIS";
    } else if(segment == "that") {
        return "THAT";
    }

    // TODO: error handling
    return NULL;
}

