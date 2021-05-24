class VMWriter:
    def __init__(self, infile):
        self.outfile = open(infile, 'w')

    def writeFunction(self, cn, sn, nLocals):
        self.outfile.write(f'function {cn}.{sn} {nLocals}\n')

    def writeCall(self, name, nArgs):
        self.outfile.write(f'call {name} {nArgs}\n')

    def writePush(self, segment, index):
        self.outfile.write(f'push {segment} {index}\n')

    def writePop(self, segment, index):
        self.outfile.write(f'pop {segment} {index}\n')
    
    def writeArithmetic(self, command):
        self.outfile.write(f'{command}\n')

    def writeReturn(self):
        self.outfile.write(f'return\n')

    def writeLabel(self, label):
        self.outfile.write(f'label L{label}\n')

    def writeGoto(self, label):
        self.outfile.write(f'goto L{label}\n')

    def writeIf(self, label):
        self.outfile.write(f'if-goto L{label}\n')
