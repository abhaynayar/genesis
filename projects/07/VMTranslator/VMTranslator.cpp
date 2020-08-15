#include <iostream>
#include <fstream>
#include "Enum.h"
#include "Parser.h"
#include "CodeWriter.h"

int main(int argc, char** argv) {

    if(argc < 2) {
        std::cout << "Pass input file as argument\n";
        return -1;
    }

    Parser parser(argv[1]);
    CodeWriter codewriter(argv[1]);
    
    while(parser.hasMoreCommands()) {
        parser.advance();
        
        // comments are automatically disregarded
        // for now, but create a mechanism later on
        switch(parser.commandType()) {
            case C_ARITHMETIC:
                // arg1() will contain cmd in case of add
                codewriter.writeArithmetic(parser.arg1());
                break;
            case C_PUSH:
                codewriter.writePushPop(C_PUSH, 
                        parser.arg1(), parser.arg2());
                break;
            case C_POP:
                codewriter.writePushPop(C_POP, 
                        parser.arg1(), parser.arg2());
                break;
        }
    }
    
    return 0;
}

