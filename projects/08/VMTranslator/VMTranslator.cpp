#include <iostream>
#include <fstream>
#include "Enum.h"
#include "Parser.h"
#include "CodeWriter.h"

/*
 *  HOW THE STACK LOOKS LIKE
 *
 *  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *      caller's working stack
 *      arguments passed to the callee <- @ARG
 *      caller's stack frame
 *          - return address
 *          - LCL
 *          - ARG
 *          - THIS
 *          - THAT
 *      callee's local variables <- @LCL
 *  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 *  Testing order:
 *   - BasicLoop
 *   - Fibonacci Series
 *   - SimpleFunction
 *   - NestedCall
 *   - FibonacciElement
 *   - StaticsTest
 */

int main(int argc, char** argv) {

    if(argc < 2) {
        puts("usage: VMTranslator [inputFile.vm/directoryName]");
        return 1;
    }

    Parser parser(argv[1]);
    CodeWriter codewriter(argv[1]);
    
    while(parser.hasMoreCommands()) {
        parser.advance();
        
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
                codewriter.writeFunction(parser.arg1(), parser.arg2());
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
    
    return 0;
}

