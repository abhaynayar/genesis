import pprint

class SymbolTable:
    def __init__(self):
        self.ct = {}
        self.st = {}


    def printTables(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.ct)
        pp.pprint(self.st)


    # clear the subroutine-level symbol table on
    # encountering a new subroutine declaration
    def startSubroutine(self):
        self.st.clear()
        return


    # returns number of variables of given kind
    def varCount(self, kind):
        ans = 0
        for symbol in self.ct:
            if self.ct[symbol]['kind'] == kind:
                ans += 1

        for symbol in self.st:
            if self.st[symbol]['kind'] == kind:
                ans += 1
        return ans
    

    def define(self, name, type, kind):
        # this function is going to be used when variables are declared:
        # compileVarDec, compileClassVarDec, compileParameterList
        # compileSubroutine (for adding current object in methods)

        index = self.varCount(kind)
        
        # name => identifier
        # type => int / char / bool / className
        # kind => static / field / arg / local (var)
        # index => needs to be computed for every KIND
        # scope => class / subroutine

        if kind in ['STATIC', 'FIELD']:
            self.ct[name] = {
                'type': type,
                'kind': kind,
                'index': index
            }
        
        elif kind in ['VAR', 'ARG']:
            self.st[name] = {
                'type': type,
                'kind': kind,
                'index': index
            }


    def kindOf(self, name):
        if name in self.ct:
            return self.ct[name]['kind']
        elif name in self.st:
            return self.st[name]['kind']


    def typeOf(self, name):
        if name in self.ct:
            return self.ct[name]['type']
        elif name in self.st:
            return self.st[name]['type']


    def indexOf(self, name):
        if name in self.ct:
            return self.ct[name]['index']
        elif name in self.st:
            return self.st[name]['index']

