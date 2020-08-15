#include <fstream>
#include <iostream>
#include <regex>

#include "Enum.h"
#include "Parser.h"

// opens input file
Parser::Parser(std::string filename) {
    // TODO: handle directories
    infile.open(filename);
}

// check if file stream is empty
bool Parser::hasMoreCommands() {
    return infile.peek() != std::ifstream::traits_type::eof();
}

// read next command from the input and make it current
void Parser::advance() {
    std::getline(infile,currentCommand);

    // TODO: remove whitespace and comments

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
    // ASSUMING: there is no whitespace before the command token
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
    } else if(cmd == "label") {
        return C_LABEL;
    } else if(cmd == "goto") {
        return C_GOTO;
    } else if(cmd == "if-goto") {
        return C_IF;
    } else if(cmd == "function") {
        return C_FUNCTION;
    } else if(cmd == "return") {
        return C_RETURN;
    } else if(cmd == "call") {
        return C_CALL;
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
    // only call for PUSH, POP, FUNCTION, CALL
    
    // TODO: use regex in other parsing functions as well
    std::regex reg("\\s+"); // use whitespace as delimiter
    std::sregex_token_iterator iter(currentCommand.begin(), 
            currentCommand.end(), reg, -1);
    std::sregex_token_iterator end;
    std::vector<std::string> v(iter, end);
    return stoi(v[2]);
}

Parser::~Parser() {
    if(infile.is_open()) {
        infile.close();
    }
}

