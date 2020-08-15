class CodeWriter {

private:
    std::ofstream outfile;
    int labelCounter;
    std::string fnNoExt; // TODO: change this to moduleName

public:

    // part1
    CodeWriter(std::string fileName);
    void writeArithmetic(std::string cmd);
    void writePushPop(int cmd, std::string segment, int index);
    std::string registerName(std::string segment);
    ~CodeWriter();
    
    // part2
    void setFileName(std::string fileName); // inform writer of new file
    void writeInit(); // bootstrap assembly code to initialize the vm

    // branching commands
    void writeLabel(std::string label);
    void writeGoto(std::string label);
    void writeIf(std::string label);

    // function commands
    void writeFunction(std::string functionName, int numVars);
    void writeCall(std::string functionName, int numArgs);
    void writeReturn();

};

