#include <fstream>
#include <iostream>
#include "Parser.h"
#include "CodeWriter.h"
#include "CommandType.h"

#include <experimental/filesystem>
namespace fs = std::experimental::filesystem;

/*
 *  Testing project8:
 *   - (done) BasicLoop
 *   - (done) Fibonacci Series
 *   - (done) SimpleFunction
 *   - (done) NestedCall
 *   - (done) FibonacciElement
 *   - StaticsTest
 */

int main(int argc, char** argv) {
    
    if(argc != 2) {
        puts("usage: VMTranslator [inputFile.vm/directoryName]");
        return 1;
    }

    std::string arg1(argv[1]); 
    fs::path path(arg1);
    bool isdir = false;
    std::vector<std::string> files;
    
    if(fs::is_directory(path)) {
        isdir = true;
        for(const auto &entry : fs::directory_iterator(path)) {
            std::string vm_file(entry.path());
            if(vm_file.substr(vm_file.find_last_of(".")+1) == "vm") {
                files.push_back(entry.path());
            }
        }
    } else {
        // ASSUMPTION: individual files have ".vm" extension
        files.push_back(path);
    }

    CodeWriter codewriter;
    Parser parser;

    for(std::string path: files) {
        
        codewriter.resetFileStream();
        codewriter.setFileName(path);

        parser.resetFileStream();
        parser.setFileName(path);
        
        while(parser.hasMoreCommands()) {
            parser.advance();
            switch(parser.commandType()) {
                case C_ARITHMETIC:
                    // arg1() will contain cmd in case of ARITHMETIC
                    codewriter.writeArithmetic(parser.arg1());
                    break;
                
                case C_PUSH:
                    codewriter.writePushPop(C_PUSH, parser.arg1(),
                            parser.arg2());
                    break;
                
                case C_POP:
                    codewriter.writePushPop(C_POP, parser.arg1(),
                            parser.arg2());
                    break;

                case C_LABEL:
                    codewriter.writeLabel(parser.arg1());
                    break;
                
                case C_GOTO:
                    codewriter.writeGoto(parser.arg1());
                    break;

                case C_IF:
                    codewriter.writeIf(parser.arg1());
                    break;

                case C_FUNCTION:
                    codewriter.writeFunction(parser.arg1(),
                            parser.arg2());
                    break;
                
                case C_RETURN:
                    codewriter.writeReturn();
                    break;
                
                case C_CALL:
                    codewriter.writeCall(parser.arg1(), parser.arg2());
                    break;
                
                default:
                    // the parser will return -1 for lines without
                    // a valid command before the first space so the 
                    // comments and whitespace will be ignored
                    break;
            }
        }
    }

    // if user gave us a directory, translate *.vm to *.asm
    // then using the below code merge *.asm to dirname.asm
    // TODO: should I delete the intermediate *.asm files?
    if(isdir == true) {

        // generating outfile path
        std::ofstream outfile;
        std::string ppath = path.parent_path();
        std::string dirname = ppath.substr(ppath.find_last_of("/"));
        outfile.open(ppath + dirname + ".asm");
        outfile << "// bootstrap code\n"
                   "@256\n"
                   "D=A\n"
                   "@SP\n"
                   "M=D\n"
                   "// call Sys.init 0\n"
                   "@LABEL0\n"
                   "D=A\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n"
                   "@LCL\n"
                   "D=M\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n"
                   "@ARG\n"
                   "D=M\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n"
                   "@THIS\n"
                   "D=M\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n"
                   "@THAT\n"
                   "D=M\n"
                   "@SP\n"
                   "A=M\n"
                   "M=D\n"
                   "@SP\n"
                   "M=M+1\n"
                   "@SP\n"
                   "D=M\n"
                   "@0\n"
                   "D=D-A\n"
                   "@5\n"
                   "D=D-A\n"
                   "@ARG\n"
                   "M=D\n"
                   "@SP\n"
                   "D=M\n"
                   "@LCL\n"
                   "M=D\n"
                   "@Sys.init\n"
                   "0;JMP\n"
                   "(LABEL0)\n";

        outfile << std::endl;
        // ASSUMPTION: the directory contains only relevant asm files
        for(const auto &entry : fs::directory_iterator(path)) {
            std::string asm_file(entry.path());
            if(asm_file.substr(asm_file.find_last_of(".")+1) == "asm"
                    && asm_file != ppath + dirname + ".asm") {
                
                std::ifstream infile;
                infile.open(asm_file);
                outfile << "// ASM_FILE: " << 
                    asm_file.substr(asm_file.find_last_of("/")+1) << "\n";
                // copy file by character
                char ch;
                while (infile.get(ch)) {
                    outfile << ch;
                }
                outfile << "\n";
            }
        }
    }

    return 0;
}

