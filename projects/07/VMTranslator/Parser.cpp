#include <fstream>
#include <iostream>
#include "Enum.h"
#include "Parser.h"

Parser::Parser(std::string filename) {
    // open input file
    infile.open(filename);
}

bool Parser::hasMoreCommands() {
    // check if file stream still has something
    return infile.peek() != std::ifstream::traits_type::eof();
}

void Parser::advance() {
    // read next command from the
    // input and make it the current
    std::getline(infile,currentCommand);

    // incase we take the source from another os
    // fix crlf issue: \r remains after getline
    if(currentCommand.back() == '\r') {
        currentCommand.pop_back();
    }
}

int Parser::commandType() {
    // search for a space, in case there is no space
    // we may have an arithmetic command for which
    // we can use the same position (end of line)
    // since there will be no further arguments
    int space = currentCommand.find(" ");
    
    // extract commandType string
    std::string cmd = currentCommand.substr(0,space);
    
    // change string to enumeration
    if(cmd == "add" || cmd == "sub" || cmd == "neg" ||
            cmd == "eq" || cmd == "gt" || cmd == "lt" ||
            cmd == "and" || cmd == "or" || cmd == "not") {
        return C_ARITHMETIC;
    } else if(cmd == "push") {
        return C_PUSH;
    } else if(cmd == "pop") {
        return C_POP;
    }

    return -1;
}

std::string Parser::arg1() {
    // return first arg of current command
    // C_ARITHMETIC: return cmd itself
    // C_RETURN: should not be called

    int space1 = currentCommand.find(" ");
    int space2 = currentCommand.find(" ", space1+1);

    // for C_ARITHMETIC commands
    if(space1 == -1 && space2 == -1) {
        return currentCommand;
    }
    
    return currentCommand.substr(space1+1, space2-(space1+1));
}

int Parser::arg2() {
    // return second arg of current command
    // only for PUSH, POP, FUNCTION, CALL
    int space = currentCommand.find_last_of(" ");
    return stoi(currentCommand.substr(space+1));
}

Parser::~Parser() {
    infile.close();
}

