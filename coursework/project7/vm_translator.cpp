#include <iostream>
#include <fstream>

enum CommandType {
    C_ARITHMETIC, C_PUSH, C_POP,
    C_LABEL, C_GOTO, C_IF,
    C_FUNCTION, C_RETURN, C_CALL
};

class Parser {
private:
    std::ifstream infile;
    std::string currentCommand;

public:
    Parser(std::string filename) {
        // open given input file
        infile.open(filename);
    }

    bool hasMoreCommands() {
        return infile.peek() != std::ifstream::traits_type::eof();
    }

    void advance() {
        // read next command from the
        // input and make it the current
        std::getline(infile,currentCommand);
    }

    int commandType() {
        // search for a space, in case there is no space
        // we may have an arithmetic command for which
        // we can use the same position (end of line)
        // since there will be no further arguments
        int space = currentCommand.find(" ");
        
        // extract commandType string
        std::string commandToken = currentCommand.substr(0,space);
        return commandTypeEnum(commandToken);
    }

    std::string arg1() {
        // return first arg of current command
        // C_ARITHMETIC: return cmd itself
        // C_RETURN: should not be called

        int space1 = currentCommand.find(" ");
        int space2 = currentCommand.find(" ", space1+1);

        // for C_ARITHMETIC commands
        if(space1 == -1 && space2 == -1) {
            return currentCommand;
        }
        
        return currentCommand.substr(space1+1, space2-space1);
    }

    int arg2() {
        // return second arg of current command
        // only for PUSH, POP, FUNCTION, CALL
        int space = currentCommand.find_last_of(" ");
        return stoi(currentCommand.substr(space+1));
    }

    ~Parser() {
        infile.close();
    }

    // auxiliary functions
    int commandTypeEnum(std::string cmd) {
        if(cmd == "add" or cmd == "sub" or cmd == "neg" or
                cmd == "eq" or cmd == "gt" or cmd == "lt" or
                cmd == "and" or cmd == "or" or cmd == "not") {
            return C_ARITHMETIC;
        }

        if(cmd == "push") {
            return C_PUSH;
        }

        if(cmd == "pop") {
            return C_POP;
        }

        return -1;
    }

};

class CodeWriter {
private:
    std::ofstream outfile;

public:
    CodeWriter(std::string filename) {
        // create output file xxx.vm for xxx.asm
        int period = filename.find_last_of(".");
        outfile.open(filename.substr(0,period) + ".asm");
    }

    // remember to write vm code as a comment in asm
    void writeArithmetic(std::string cmd) {
        // write corresponding asm to file
    }

    void writePushPop(int cmd, std::string segment, int index) {
    }

    ~CodeWriter() {
        outfile.close();
    }

};

int main(int argc, char** argv) {

    // file name to be provided
    // as command line argument
    if(argc < 2) {
        return -1;
    }

    Parser parser(argv[1]);
    CodeWriter codewriter(argv[1]);
    
    while(parser.hasMoreCommands()) {
        parser.advance();
        
        switch(parser.commandType()) {
            case C_ARITHMETIC:
                // arg1() will contain cmd
                std::cout << parser.arg1() << std::endl;
                break;
            case C_PUSH:
                std::cout << "push " << parser.arg1() 
                    << " " << parser.arg2() << std::endl;
                break;
            case C_POP:
                std::cout << "pop " << parser.arg1() 
                    << " " << parser.arg2() << std::endl;
                break;
        }
    }
    
    return 0;
}

