# by default makefile compiles the first target
# but we can use another target: $make other_target

all: VMTranslator

VMTranslator: VMTranslator.o Parser.o CodeWriter.o
	g++ -o VMTranslator -std=c++17 VMTranslator.o Parser.o CodeWriter.o -lstdc++fs

VMTranslator.o: VMTranslator.cpp
	g++ -c VMTranslator.cpp

Parser.o: Parser.cpp
	g++ -c Parser.cpp

CodeWriter.o: CodeWriter.cpp
	g++ -c CodeWriter.cpp

# make clean
clean:
	rm *.o VMTranslator

