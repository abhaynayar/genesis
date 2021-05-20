class CodeWriter {

private:
    std::ofstream outfile;
    int labelCounter;
    std::string fnNoExt;

public:
    CodeWriter(std::string);
    void writeArithmetic(std::string);
    void writePushPop(int, std::string, int);
    std::string registerName(std::string);
    ~CodeWriter();
};

