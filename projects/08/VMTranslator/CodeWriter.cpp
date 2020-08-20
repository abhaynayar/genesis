#include <fstream>
#include <iostream>
#include "CodeWriter.h"
#include "CommandType.h"

// initialize label counter for auxiliary purposes
CodeWriter::CodeWriter() {
    // LABEL0 is used for bootstrap
    labelCounter = 1;
}

// close input file
void CodeWriter::resetFileStream() {
    if(outfile.is_open()) {
        outfile.close();
    }
}

// CodeWriter only handles individual files
// directories are handled by driver (main)
void CodeWriter::setFileName(std::string path) {
    
    // removing extension from the path
    // CONTRACT: path contains ".vm" at the end
    std::string filenameWx = path.substr(0,path.find_last_of("."));
    
    // vm static variables shouldn't contain path
    int last_slash = filenameWx.find_last_of("/");
    moduleName = filenameWx.substr(last_slash+1);
       
    outfile.open(filenameWx + ".asm");
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
            // "@" + moduleName + "." + index
            outfile << "@" << moduleName << "." << index << "\n"
                       "D=M\n"
                       "@SP\n"
                       "A=M\n"
                       "M=D\n"
                       "@SP\n"
                       "M=M+1\n";
        }
    
    } else if(cmd == C_POP) {
        
        // writing vm code as a comment
        outfile << "// pop " << segment << " " << index << std::endl;
        
        // NOTE: can't pop into CONSTANT
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

            // "@" + moduleName + "." + index
            outfile << "@SP\n"
                       "M=M-1\n"
                       "A=M\n"
                       "D=M\n"
                       "@" << moduleName << "." << index << "\n"
                       "M=D\n";
        }
    }
    
    outfile << std::endl;
}

// map segment-token (from vm-code) to segment-register (in assembly)
std::string CodeWriter::registerName(std::string segment) {
    if(segment == "local") {
        return "LCL";
    } else if(segment == "argument") {
        return "ARG";
    } else if(segment == "this") {
        return "THIS";
    } else { //if(segment == "that") {
        return "THAT";
    }
}

void CodeWriter::writeLabel(std::string label) {
    outfile << "// label " << label << "\n"
               "(" << label << ")\n";
    
    outfile << std::endl;
}

void CodeWriter::writeGoto(std::string label) {
    outfile << "// goto " << label << "\n"
               "@" << label << "\n"
               "0;JMP\n";

    outfile << std::endl;
}

void CodeWriter::writeIf(std::string label) {
    // CONTRACT: we have to pop condition on top of the stack
    // true==-1 and false==0
    outfile << "// if-goto " << label << "\n"
               "@SP\n"
               "M=M-1\n"
               "A=M\n"
               "D=M\n"
               "@" << label << "\n"
               "D;JNE\n";

    outfile << std::endl;
}

void CodeWriter::writeFunction(std::string functionName, int numVars) {
    outfile << "// function " << functionName << " " << numVars << "\n"
               "(" << functionName << ")\n"
               "@" << numVars << "\n"
               "D=A\n"
               "(LABEL" << labelCounter++ << ")\n"
               "@LABEL" << labelCounter-- << "\n"
               "D;JEQ\n"
               
               // nArgs times:
               // push constant 0
               "@SP\n"
               "A=M\n"
               "M=0\n"
               "@SP\n"
               "M=M+1\n"
               "D=D-1\n"
               "@LABEL" << labelCounter++ << "\n"
               "0;JMP\n"
               "(LABEL" << labelCounter++ << ")\n";

    outfile << std::endl;
}

void CodeWriter::writeReturn() {
    outfile << "// return\n"
               // endFrame(R13) = LCL
               "@LCL\n"
               "D=M\n"
               "@R13\n"
               "M=D\n"

               // if no arg, retAddr is overwritten
               // so we have to store it beforehand
               // retAddr(R14) = *(endFrame - 5)
               "@5\n"
               "A=D-A\n"
               "D=M\n"
               "@R14\n"
               "M=D\n"

               // *ARG = pop()
               "@SP\n"
               "M=M-1\n"
               "A=M\n"
               "D=M\n"
               "@ARG\n"
               "A=M\n"
               "M=D\n"

               // SP = ARG+1
               "D=A\n"
               "@SP\n"
               "M=D+1\n"

               // THAT = *(endFrame - 1)
               "@R13\n"
               "AM=M-1\n"
               "D=M\n"
               "@THAT\n"
               "M=D\n"
                
               // THIS = *(endFrame - 2)
               "@R13\n"
               "AM=M-1\n"
               "D=M\n"
               "@THIS\n"
               "M=D\n"

               // ARG = *(endFrame - 3)
               "@R13\n"
               "AM=M-1\n"
               "D=M\n"
               "@ARG\n"
               "M=D\n"

               // LCL = *(endFrame - 4)
               "@R13\n"
               "AM=M-1\n"
               "D=M\n"
               "@LCL\n"
               "M=D\n"

               // goto retAddr
               "@R14\n"
               "A=M\n"
               "0;JMP\n";

    outfile << std::endl;
}

void CodeWriter::writeCall(std::string functionName, int numArgs) {
    outfile << "// call " << functionName << " " << numArgs << "\n";

    // push retAddr
    outfile << "@LABEL" << labelCounter <<
               "\nD=A\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n";

    // push LCL
    outfile << "@LCL\n"
               "D=M\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n";

    // push ARG
    outfile << "@ARG\n"
               "D=M\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n";

    // push THIS
    outfile << "@THIS\n"
               "D=M\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n";

    // push THAT
    outfile << "@THAT\n"
               "D=M\n"
               "@SP\n"
               "A=M\n"
               "M=D\n"
               "@SP\n"
               "M=M+1\n";

    // ARG = (SP-5)-nArgs
    outfile << "@SP\n"
               "D=M\n"
               "@" << numArgs << "\n"
               "D=D-A\n"
               "@5\n"
               "D=D-A\n"
               "@ARG\n"
               "M=D\n";
    
    // LCL = SP
    outfile << "@SP\n"
               "D=M\n"
               "@LCL\n"
               "M=D\n";
    
    // goto functionName
    outfile << "@" << functionName << "\n"
               "0;JMP\n";

    // (retAddr)
    outfile << "(LABEL" << labelCounter++ << ")\n";
    outfile << std::endl;

}

