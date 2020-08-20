class CodeWriter {

private:
    int labelCounter;
    std::ofstream outfile;
    std::string moduleName;

public:
    // part1
    CodeWriter();
    void resetFileStream();
    void writeArithmetic(std::string cmd);
    void writePushPop(int cmd, std::string segment, int index);
    std::string registerName(std::string segment);
    
    // part2
    void setFileName(std::string fileName); // inform writer of new file
    void writeLabel(std::string label);
    void writeGoto(std::string label);
    void writeIf(std::string label);
    void writeFunction(std::string functionName, int numVars);
    void writeCall(std::string functionName, int numArgs);
    void writeReturn();

};

