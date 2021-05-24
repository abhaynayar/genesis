import html
import VMWriter
import JackType
import SymbolTable
import JackTokenizer
import xml.dom.minidom as xml


# NOTE:
# - remove XML generation (at a later point in time, if possible)
# - consolidate subroutineCall from compileDoStatement and compileTerm

class CompilationEngine:
    def __init__(self, infile):
        # tokenizer
        self.initTokens(infile)

        # symbol table
        self.sym = SymbolTable.SymbolTable()
        self.currentClass = ''
        self.currentSub = ''

        # used for storing nArgs and nLocals
        self.temp = 0

        # when calling methods, to calculate number of arguments since
        # methods have an extra argument that is the calling object
        self.methodCallCheck = False

        # keep unique labels in compiled vm code
        self.L = 0

        # output to VM file
        self.vm = VMWriter.VMWriter(infile[:-5] + '.vm')

        # compilation engine - assuming class first
        classTag = self.writeTag('class', self.compileClass())

        # xml prettify
        # dom = xml.parseString(classTag)
        # pretty = dom.toprettyxml()
        # pretty = pretty.replace('<parameterList/>',
        #                         '<parameterList></parameterList>')
        # pretty = pretty.replace('<expressionList/>',
        #                         '<expressionList></expressionList>')

        # remove xml declaration
        # doc = xml.Document()
        # declaration = doc.toxml()
        
        # write to xml file
        # outfile = open(infile[:-5] + '.xml', 'w')
        # outfile.write(pretty[len(declaration)+1:])


    def initTokens(self, infile):
        self.i = 0 # token counter
        self.tokens = []
        self.tokenType = []

        jt = JackTokenizer.JackTokenizer(infile)
        while jt.hasMoreTokens():
            jt.advance()
            self.tokens.append(jt.current)
            self.tokenType.append(jt.type)


    def writeTag(self, name, content=None):
        if content == None: 
            content = self.tokens[self.i]
        self.i += 1 # increment token counter

        ans = '<'+name+'>'
        ans += content + ''
        ans += '</'+name+'>'
        return ans


    # class: 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self):
        ans = self.writeTag('keyword') # 'class'
        self.currentClass = self.tokens[self.i]
        ans += self.writeTag('identifier')
        ans += self.writeTag('symbol')

        # classVarDec*
        while self.tokens[self.i] in JackType.classvars:
            ans += self.writeTag('classVarDec', \
                    self.compileClassVarDec())
            self.i -= 1

        # subroutineDec*
        while self.tokens[self.i] in JackType.subroutines:
            ans += self.writeTag('subroutineDec', \
                   self.compileSubroutine())
            self.i -= 2

        ans += self.writeTag('symbol')
        return ans


    # classVarDec: ('static'|'field') type varName (',' varName)* ';'
    def compileClassVarDec(self):
        
        # ('static' | 'field')
        kind = self.tokens[self.i]
        ans = self.writeTag('keyword')

        # type
        type = self.tokens[self.i]
        if type in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')

        # varName
        varName = self.tokens[self.i]
        ans += self.writeTag('identifier')

        # adding to the symbol table
        self.sym.define(varName, type, kind.upper())

        # (',' varName)*
        while self.tokens[self.i] == ',': # while not semicolon
            ans += self.writeTag('symbol')
            varName = self.tokens[self.i]
            ans += self.writeTag('identifier')
            
            # adding to the symbol table
            self.sym.define(varName, type, kind.upper())

        # ';'
        ans += self.writeTag('symbol')
        return ans


    # subroutineDec: ('constructor'|'function'|'method')
    #                ('void'|type) subroutineName
    #                '(' parameterList ')' subroutineBody
    def compileSubroutine(self):
        # clear the subroutine symbol table for a new subroutine
        self.sym.startSubroutine()

        # 'constructor'|'function'|'method'
        self.subroutineType =  self.tokens[self.i]
        ans = self.writeTag('keyword')

        # 'void'|type
        type = self.tokens[self.i]
        if type in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')

        # if it is a 'method', adding 'this' as first 'ARG'
        if self.subroutineType == 'method':
            self.sym.define('this', type, 'ARG')

        # subroutineName '('
        self.currentSub = self.tokens[self.i]
        ans += self.writeTag('identifier')
        ans += self.writeTag('symbol')
        ans += self.writeTag('parameterList', \
                self.compileParameterList())
        ans += self.writeTag('symbol') # ')'
        ans += self.writeTag('subroutineBody', \
               self.compileSubroutineBody())
        return ans


    # parameterList: ( (type varName) (',' type varName)*)?
    def compileParameterList(self):
        ans = ''

        if self.tokens[self.i] != ')':
            # type
            type = self.tokens[self.i]
            if type in JackType.types:
                ans += self.writeTag('keyword')
            else: ans += self.writeTag('identifier')

            # varName
            varName = self.tokens[self.i]
            ans += self.writeTag('identifier')

            # adding to symbol table
            self.sym.define(varName, type, 'ARG')
            
            # (',' type varName)* 
            while self.tokens[self.i] == ',':
                ans += self.writeTag('symbol')

                # type
                type = self.tokens[self.i]
                if type in JackType.types:
                    ans += self.writeTag('keyword')
                else: ans += self.writeTag('identifier')

                # varName
                varName = self.tokens[self.i]
                ans += self.writeTag('identifier')

                # adding to symbol table
                self.sym.define(varName, type, 'ARG')
        
        self.i -= 1
        return ans


    # subroutineBody: '{' varDec* statements '}'
    def compileSubroutineBody(self):

        ans = self.writeTag('symbol') # '{'
        nLocals = 0

        # varDec*
        while self.tokens[self.i] == 'var':
            ans += self.writeTag('varDec', self.compileVarDec())
            nLocals += self.temp
            self.i -= 1

        # since nLocals had to figured out here, we have
        # to generate function declaration code over here
        self.vm.writeFunction(self.currentClass, self.currentSub, nLocals)
        
        # if we are using methods, we need to push the first argument on
        # to the stack and pop it into pointer so that we can access the
        # field variables of the current object
        if self.subroutineType == 'method':
            self.vm.writePush('argument', 0)
            self.vm.writePop('pointer', 0)


        # when we are declaring constructors, we need to allocate memory
        # according to the number of field variables we have in the class
        elif self.subroutineType == 'constructor':
            numFields = self.sym.varCount('FIELD')
            self.vm.writePush('constant', numFields)
            self.vm.writeCall('Memory.alloc', 1)
            self.vm.writePop('pointer', 0)


        # statements
        ans += self.writeTag('statements', self.compileStatements())
        ans += self.writeTag('symbol')
        return ans


    # statements: statement*
    def compileStatements(self):
        ans = ''
        while self.tokens[self.i] in JackType.statements:
            ans += self.compileStatement()
            self.i -= 1
            
        self.i -= 1
        return ans


    # statement: let | if | while | do | return
    def compileStatement(self):
        stype = self.tokens[self.i]
        if stype == 'let':
            return self.writeTag('letStatement', \
                   self.compileLetStatement())
        
        if stype == 'if':
            return self.writeTag('ifStatement', \
                   self.compileIfStatement())

        if stype == 'while':
            return self.writeTag('whileStatement', \
                   self.compileWhileStatement())

        if stype == 'do': 
            return self.writeTag('doStatement', \
                   self.compileDoStatement())

        if stype == 'return':
            return self.writeTag('returnStatement', \
                   self.compileReturnStatement())


    # doStatement: 'do' subroutineCall ';'
    def compileDoStatement(self):

        # 'do'
        ans = self.writeTag('keyword')
        
        # (className|varName) '.' subroutineName '(' expressionList ')'
        if self.tokens[self.i+1] == '.':
            self.methodCallCheck = False
            
            # class|varName
            cn = self.tokens[self.i]

            # if varName, change to its corresponding class
            if cn in self.sym.ct:
                self.methodCallCheck = True
                self.vm.writePush(\
                        JackType.kindSegment[self.sym.ct[cn]['kind']],\
                        self.sym.ct[cn]['index'])
                cn = self.sym.ct[cn]['type']
            elif cn in self.sym.st:
                self.methodCallCheck = True
                self.vm.writePush(\
                        JackType.kindSegment[self.sym.st[cn]['kind']],\
                        self.sym.st[cn]['index'])
                cn = self.sym.st[cn]['type']
            
            # subroutineName
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            sn = self.tokens[self.i]
            ans += self.writeTag('identifier') 
            ans += self.writeTag('symbol')
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')
            self.vm.writeCall(f'{cn}.{sn}', self.temp)

        # subroutineName '(' expressionList ')' ...
        elif self.tokens[self.i+1] == '(':
            self.methodCallCheck = True
            cn = self.currentClass
            sn = self.tokens[self.i]
            ans += self.writeTag('identifier') 
            ans += self.writeTag('symbol')
            self.vm.writePush('pointer', 0)
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')

            # these calls always mean that you are calling another method
            # within the same class, so push the object that has called
            # the method and call it using the class name
            
            # even if we're calling a function, it'll be fine to push the
            # pointer as the function won't be using the pointer segment

            self.vm.writeCall(f'{cn}.{sn}', self.temp)

        # ';'
        ans += self.writeTag('symbol')

        # discard void return value
        self.vm.writePop('temp', 0) 
        return ans


    # expression list: (expression (',' expression)* )?
    def compileExpressionList(self):
        ans = ''
        nArgs = 0

        # if a method is being called, number of arguments increases by
        # one because the object calling the method is pushed on to the
        # parameter list
        if self.methodCallCheck == True:
            nArgs = 1

        if self.tokens[self.i] != ')':
            nArgs += 1
            ans += self.writeTag('expression', self.compileExpression())

            while self.tokens[self.i] == ',':
                nArgs += 1
                ans += self.writeTag('symbol')
                ans += self.writeTag('expression', \
                        self.compileExpression())

        self.temp = nArgs
        self.i -= 1
        return ans


    # array[expression1] = expression2
    #   push array
    #   push expression1
    #   add
    #   push expression2
    #   pop temp 0
    #   pop pointer 1
    #   push temp 0
    #   pop that 0

    # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    def compileLetStatement(self):
        ans = self.writeTag('keyword') # 'let'
        
        varName = self.tokens[self.i]
        ans += self.writeTag('identifier') # varName
        kind = self.sym.kindOf(varName)
        index = self.sym.indexOf(varName)

        if self.tokens[self.i] == '[':
            
            # push var
            self.vm.writePush(JackType.kindSegment[kind], index)
            ans += self.writeTag('symbol')
            
            # push expression1
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

            # add
            self.vm.writeArithmetic('add')

            # push expression2
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

            # pop temp 0
            # pop pointer 1
            # push temp 0
            # pop that 0
            self.vm.writePop('temp', 0)
            self.vm.writePop('pointer', 1)
            self.vm.writePush('temp', 0)
            self.vm.writePop('that', 0)
        
        else:
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

            # store the value of the evaluated expression in varName
            kind = self.sym.kindOf(varName)
            index = self.sym.indexOf(varName)
            self.vm.writePop(JackType.kindSegment[kind], index)
        return ans


    # codeWrite(exp):
    #   if exp is a number n:
    #       output "push n"
    #   if exp is a variable var:
    #       output "push var"
    #   if exp is "exp1 op exp2":
    #       codeWrite(exp1)
    #       codeWrite(exp2)
    #       output "op"
    #   if exp is "op exp":
    #       codeWrite(exp)
    #       output "op"
    #   if exp is "f(exp1,exp2,...)":
    #       codeWrite(exp1)
    #       codeWrite(exp2),...,
    #       output "call f" 

    # expression: term (op term)*
    def compileExpression(self):
        ans = self.writeTag('term', self.compileTerm()) # term
        
        # (op term)*
        while html.unescape(self.tokens[self.i]) in JackType.operators:
            operator = self.tokens[self.i]
            ans += self.writeTag('symbol')
            ans += self.writeTag('term', self.compileTerm())
            self.vm.writeArithmetic(JackType.op_vm[operator])

        self.i -= 1
        return ans
 
 
    # term: integerConstant | stringConstant | keywordConstant | varName |
    #       varName '[' expression ']' | subroutineCall | '(' expression 
    #       ')' | unaryOp term
    def compileTerm(self):
        
        ans = ''
        # integerConstant
        if self.tokenType[self.i] == 'integerConstant':
            self.vm.writePush('constant', self.tokens[self.i])
            ans += self.writeTag('integerConstant')

        # stringConstant
        elif self.tokenType[self.i] == 'stringConstant':
            str1 = self.tokens[self.i]
            self.vm.writePush('constant', len(str1))
            self.vm.writeCall('String.new', 1)
            for chr1 in str1:
                self.vm.writePush('constant', ord(chr1))
                self.vm.writeCall('String.appendChar', 2)
            ans += self.writeTag('stringConstant')

        # keywordConstant (subset of keywords)
        elif self.tokens[self.i] in JackType.keywords:
            keyConst = self.tokens[self.i]
            if keyConst == 'true':
                self.vm.writePush('constant', 1)
                self.vm.writeArithmetic('neg')
            elif keyConst == 'false':
                self.vm.writePush('constant', 0)
            elif keyConst == 'this':
                self.vm.writePush('pointer', 0)
            elif keyConst == 'null':
                self.vm.writePush('constant', 0)
            ans += self.writeTag('keyword')

        # unaryOp term
        elif self.tokens[self.i] in JackType.unary:
            unary_op = self.tokens[self.i]
            ans += self.writeTag('symbol')
            ans += self.writeTag('term', self.compileTerm())
            self.vm.writeArithmetic(JackType.unary_vm[unary_op])

        # '(' expression ')'
        elif self.tokens[self.i] == '(':
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

        # varName '[' expression ']'
        elif self.tokens[self.i+1] == '[':
            varName = self.tokens[self.i]
            ans += self.writeTag('identifier')
            kind = self.sym.kindOf(varName)
            index = self.sym.indexOf(varName)

            # push varName
            self.vm.writePush(JackType.kindSegment[kind], index)
            ans += self.writeTag('symbol')

            # push expression; (=index)
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

            # add
            self.vm.writeArithmetic('add')

            # pop pointer 1
            self.vm.writePop('pointer', 1)

            # push that 0
            self.vm.writePush('that', 0)


        # (className|varName) '.' subroutineName '(' expressionList ')'
        elif self.tokens[self.i+1] == '.':
            self.methodCallCheck = False

            # class|varName
            cn = self.tokens[self.i]
            
            # if varName, change to its corresponding class
            if cn in self.sym.ct:
                self.methodCallCheck = True
                self.vm.writePush(\
                        JackType.kindSegment[self.sym.ct[cn]['kind']],\
                        self.sym.ct[cn]['index'])
                cn = self.sym.ct[cn]['type']
            elif cn in self.sym.st:
                self.methodCallCheck = True
                self.vm.writePush(\
                        JackType.kindSegment[self.sym.st[cn]['kind']],\
                        self.sym.st[cn]['index'])
                cn = self.sym.st[cn]['type']

            # subroutineName
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            sn = self.tokens[self.i]
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')
            self.vm.writeCall(f'{cn}.{sn}', self.temp)

        # subroutineName '(' expressionList ')' ...
        elif self.tokens[self.i+1] == '(':
            self.methodCallCheck = True
            cn = self.currentClass
            sn = self.tokens[self.i]
            ans += self.writeTag('identifier') 
            ans += self.writeTag('symbol')
            self.vm.writePush('pointer', 0)
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')
            self.vm.writeCall(f'{cn}.{sn}', self.temp)

        # varName
        else:
            # to push a var, first search for it in the symbol table
            # then push it according to its segment and index number
            varName = self.tokens[self.i]
            kind = self.sym.kindOf(varName)
            index = self.sym.indexOf(varName)

            # to update variables use POP in letStatements
            # don't need TYPE when generating code: typeless
            self.vm.writePush(JackType.kindSegment[kind], index)
            ans += self.writeTag('identifier')
        
        self.i -= 1
        return ans


    # if-statement:
    #   compiled(expression)
    #   not
    #   if-goto L1
    #   compiled(statments)
    #   goto L2
    # label L1
    #   compiled(statements)
    # label L2
    #   ...

    # ifStatement: 'if' '(' expression ')' '{' statements '}'
    #               ( 'else' '{' statements '}' )?
    def compileIfStatement(self):
        ans = self.writeTag('keyword') # 'if'
        ans += self.writeTag('symbol') # '('
        ans += self.writeTag('expression', self.compileExpression())

        L = self.L
        self.vm.writeArithmetic('not')
        self.vm.writeIf(L+1)

        ans += self.writeTag('symbol') # ')'
        ans += self.writeTag('symbol') # '{'

        self.L += 2
        ans += self.writeTag('statements', self.compileStatements())

        self.vm.writeGoto(L+2)
        self.vm.writeLabel(L+1)
        ans += self.writeTag('symbol') # '}'
        
        if self.tokens[self.i] == 'else':
            ans += self.writeTag('keyword') # 'else'
            ans += self.writeTag('symbol') # '{'
            self.L += 2
            ans += self.writeTag('statements', self.compileStatements())
            ans += self.writeTag('symbol') # '}'
        
        self.vm.writeLabel(L+2)
        return ans


    # label L1
    #   compiled(expression)
    #   not
    #   if-goto L2
    #   compiled(statements)
    #   goto L1
    # labelL2
    #   ...

    # whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compileWhileStatement(self):
        
        L = self.L
        self.vm.writeLabel(L+1)
        ans = self.writeTag('keyword') # 'while'
        ans += self.writeTag('symbol') # '('
        ans += self.writeTag('expression', self.compileExpression())
        
        self.vm.writeArithmetic('not')
        self.vm.writeIf(L+2)
        
        ans += self.writeTag('symbol') # ')'
        ans += self.writeTag('symbol') # '{'
        self.L += 2
        ans += self.writeTag('statements', self.compileStatements())
        ans += self.writeTag('symbol')

        self.vm.writeGoto(L+1)
        self.vm.writeLabel(L+2)
        return ans


    # returnStatment: 'return' expression? ';'
    def compileReturnStatement(self):
        
        ans = ''
        ans += self.writeTag('keyword')
        if self.tokens[self.i] == ';':
            self.vm.writePush('constant', 0)
            ans += self.writeTag('symbol')
        else:
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')
        
        self.vm.writeReturn()
        return ans


    # varDec: 'var' type varName (',' varName)* ';'
    def compileVarDec(self):

        # since we are already here, we have at least one variable
        self.temp = 1 # acts as nLocals

        # 'var'
        ans = self.writeTag('keyword', 'var')        

        # type
        type = self.tokens[self.i] 
        if type in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')

        # varName
        varName = self.tokens[self.i]
        ans += self.writeTag('identifier')
        self.sym.define(varName, type, 'VAR')

        # for single variable declaration
        if self.tokens[self.i] == ';':
            ans += self.writeTag('symbol')
            return ans

        # (',' varName)* ';'
        while self.tokens[self.i] != ';':
            if self.tokens[self.i] == ',':
                self.temp += 1
                ans += self.writeTag('symbol')
            else:
                varName = self.tokens[self.i]
                self.sym.define(varName, type, 'VAR')
                ans += self.writeTag('identifier')

        ans += self.writeTag('symbol')
        return ans
