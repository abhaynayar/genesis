#include <iostream>
#include <fstream>

#include "Enum.h"
#include "Parser.h"
#include "CodeWriter.h"

/*
 *  TODO: 12th august 2020
 *  0.  You have already handled the constant segment;
 *  1.  Next, handle the four segments local, argument, this, and that;
 *  2.  Next, handle the pointer and temp segments, in particular allowing modification of thebases of the this and that segments;
 *  3.  Finally, handle the static segment.
 */

int main(int argc, char** argv) {

    if(argc < 2) {
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
                break;
        }
    }
    
    return 0;
}

