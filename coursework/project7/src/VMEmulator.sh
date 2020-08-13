#!/bin/bash
g++ -c main.cpp
g++ -c Parser.cpp
g++ -c CodeWriter.cpp
g++ -o main main.o Parser.o CodeWriter.o
./main $1
rm main main.o Parser.o CodeWriter.o

