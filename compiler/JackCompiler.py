import JackTokenizer
import CompilationEngine

import os
import sys
import glob

def list_files(directory, extension):
    return (f for f in os.listdir(directory) \
            if f.endswith('.' + extension))

# input should be a single "*.jack" file
def handleSingleFile(infile):
    print(infile)
    ce = CompilationEngine.CompilationEngine(infile)

def main():
    if len(sys.argv) != 2:
        print('Usage: JackCompiler [file/directory]')
        exit()

    # path to a single source file
    if os.path.isfile(sys.argv[1]) == True:
        if sys.argv[1].endswith('.jack'):
            handleSingleFile(sys.argv[1])
    
    # directory containing source file(s)
    elif os.path.isdir(sys.argv[1]) == True:
        for file in list_files(sys.argv[1], 'jack'):
            handleSingleFile(sys.argv[1] + '/' + file)
    else: print('Invalid file/directory')
        

if __name__ == '__main__':
    main()
