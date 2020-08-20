class Parser {
private:
    std::ifstream infile;
    std::string currentCommand;
public:
    void resetFileStream();
    void setFileName(std::string);
    bool hasMoreCommands();
    void advance();
    
    int commandType();
    std::string arg1();
    int arg2();
};

