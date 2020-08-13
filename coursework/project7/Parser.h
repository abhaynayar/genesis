class Parser {
private:
    std::ifstream infile;
    std::string currentCommand;
public:
    Parser(std::string);
    ~Parser();

    bool hasMoreCommands();
    void advance();
    
    int commandType();
    std::string arg1();
    int arg2();
};

