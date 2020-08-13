class CodeWriter {

private:
    std::ofstream outfile;
    int labelCounter;

public:
    CodeWriter(std::string);
    ~CodeWriter();

    void writeArithmetic(std::string);
    void writePushPop(int, std::string, int);
};

