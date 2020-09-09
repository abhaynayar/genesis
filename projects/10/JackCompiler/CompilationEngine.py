import JackType
import JackTokenizer
# import lxml.etree as etree
import xml.dom.minidom as xml
import html


class CompilationEngine:
    def __init__(self, infile):
        
        # tokenizer
        self.initTokens(infile)

        # compilation engine - assuming class first
        classTag = self.writeTag('class', self.compileClass())

        # root = etree.fromstring(classTag)
        # pretty = etree.tostring(root, pretty_print=True).decode()
        
        # xml prettify
        dom = xml.parseString(classTag)
        print('CLASS parsed')

        pretty = dom.toprettyxml()
        pretty = pretty.replace('<parameterList/>',
                '<parameterList>\n</parameterList>')
        pretty = pretty.replace('<expressionList/>',
                '<expressionList>\n</expressionList>')

        # remove xml declaration
        doc = xml.Document()
        declaration = doc.toxml()
        
        # NOTE: remember to change ".xml" to ".xyz when debugging
        print('OUT:', infile[:-5] + '.xml')
        outfile = open(infile[:-5] + '.xml', 'w')
        outfile.write(pretty[len(declaration)+1:])


    def initTokens(self, infile):
        # NOTE: no need to write token file
        # tfile = open(infile[:-5] + 'T.xyz', 'w')
        # tfile.write('<tokens>\n')
        
        self.i = 0 # token counter
        self.tokens = []
        self.token_type = []

        jt = JackTokenizer.JackTokenizer(infile)
        while jt.hasMoreTokens():
            jt.advance()
            # tfile.write('<' + jt.type + '>')
            # tfile.write(jt.current)
            # tfile.write('</' + jt.type + '>\n')
            self.tokens.append(jt.current)
            self.token_type.append(jt.type)
        
        # tfile.write('</tokens>\n')
        # tfile.close()


    def writeTag(self, name, content=None):
        if content == None: 
            content = self.tokens[self.i]
        self.i += 1 # increment token counter

        ans = ''
        ans += '<'+name+'>'
        ans += content + ''
        ans += '</'+name+'>'
        return ans


    # class: 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self):
        ans = ''
        ans += self.writeTag('keyword')
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
        ans = ''

        # ('static' | 'field')
        ans += self.writeTag('keyword')

        # type
        if self.tokens[self.i] in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')

        # varName
        ans += self.writeTag('identifier')

        # (',' varName)*
        while self.tokens[self.i] == ',': # while not semicolon
            ans += self.writeTag('symbol')
            ans += self.writeTag('identifier')

        # ';'
        ans += self.writeTag('symbol')
        return ans


    # subroutineDec: ('constructor'|'function'|'method')
    #                ('void'|type) subroutineName
    #                '(' parameterList ')' subroutineBody
    def compileSubroutine(self):
        ans = ''

        # cfm vt subroutineName '('
        ans += self.writeTag('keyword')

        if self.tokens[self.i] in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')
        ans += self.writeTag('identifier')
        ans += self.writeTag('symbol')
        
        ans += self.writeTag('parameterList', \
               self.compileParameterList())
        
        # ')'
        ans += self.writeTag('symbol')
        ans += self.writeTag('subroutineBody', \
               self.compileSubroutineBody())
        return ans

    # parameterList: ( (type varName) (',' type varName)*)?
    def compileParameterList(self):
        ans = ''
        if self.tokens[self.i] != ')':
            if self.tokens[self.i] in JackType.types:
                ans += self.writeTag('keyword')
            else: ans += self.writeTag('identifier')
            ans += self.writeTag('identifier')

            while self.tokens[self.i] == ',':
                ans += self.writeTag('symbol')
                if self.tokens[self.i] in JackType.types:
                    ans += self.writeTag('keyword')
                else: ans += self.writeTag('identifier')
                ans += self.writeTag('identifier')

        self.i -= 1
        return ans


    # subroutineBody: '{' varDec* statements '}'
    def compileSubroutineBody(self):
        ans = ''

        # '{'
        ans += self.writeTag('symbol')

        # varDec*
        while self.tokens[self.i] == 'var':
            ans += self.writeTag('varDec', self.compileVarDec())
            self.i -= 1 # don't know why this works, but it does
            # self.writeTag('symbol')

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
        ans = self.writeTag('keyword')

        # subroutineCall
        ans += self.writeTag('identifier')
        if self.tokens[self.i] == '.':
            ans += self.writeTag('symbol')
            ans += self.writeTag('identifier')
        
        # ()
        ans += self.writeTag('symbol')
        ans += self.writeTag('expressionList', \
                self.compileExpressionList())
        ans += self.writeTag('symbol')

        # ';'
        ans += self.writeTag('symbol')
        return ans


    #  expression list: (expression (',' expression)* )?
    def compileExpressionList(self):
        ans = ''
        if self.tokens[self.i] != ')':
            ans += self.writeTag('expression', \
                    self.compileExpression())
            while self.tokens[self.i] == ',':
                ans += self.writeTag('symbol')
                ans += self.writeTag('expression', \
                        self.compileExpression())

        self.i -= 1
        return ans


    # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    def compileLetStatement(self):
        ans = ''
        ans += self.writeTag('keyword')
        ans += self.writeTag('identifier')

        if self.tokens[self.i] == '[':
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

        ans += self.writeTag('symbol')
        ans += self.writeTag('expression', self.compileExpression())
        ans += self.writeTag('symbol')
        return ans


    # expression: term (op term)*
    def compileExpression(self):
        ans = ''
        ans += self.writeTag('term', self.compileTerm())
        
        # (op term)*
        while html.unescape(self.tokens[self.i]) in JackType.operators:
            ans += self.writeTag('symbol')
            ans += self.writeTag('term', self.compileTerm())

        self.i -= 1
        return ans


    # term: integerConstant | stringConstant | keywordConstant | varName |
    #       varName '[' expression ']' | subroutineCall | '(' expression 
    #       ')' | unaryOp term
    def compileTerm(self):
        ans = ''
        # integerConstant
        if self.token_type[self.i] == 'integerConstant':
            ans += self.writeTag('integerConstant')

        # stringConstant
        elif self.token_type[self.i] == 'stringConstant':
            ans += self.writeTag('stringConstant')

        # keywordConstant (subset of keywords)
        elif self.tokens[self.i] in JackType.keywords:
            ans += self.writeTag('keyword')

        # unaryOp term
        elif self.tokens[self.i] in JackType.unary:
            ans += self.writeTag('symbol')
            ans += self.writeTag('term', self.compileTerm())

        # '(' expression ')'
        elif self.tokens[self.i] == '(':
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

        # varName[]
        elif self.tokens[self.i+1] == '[':
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')

        # subroutineCall: subroutineName '(' expressionList ')' |
        #   (className|varName) '.' subroutineName '(' expressionList ')'
        elif self.tokens[self.i+1] == '(':
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')

        elif self.tokens[self.i+1] == '.':
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            ans += self.writeTag('identifier')
            ans += self.writeTag('symbol')
            ans += self.writeTag('expressionList', \
                    self.compileExpressionList())
            ans += self.writeTag('symbol')

        # varName
        else: ans += self.writeTag('identifier')
        self.i -= 1
        return ans


    # ifStatement: 'if' '(' expression ')' '{' statements '}'
    #               ( 'else' '{' statements '}' )?
    def compileIfStatement(self):
        ans = ''
        ans += self.writeTag('keyword')
        ans += self.writeTag('symbol')
        ans += self.writeTag('expression', self.compileExpression())
        ans += self.writeTag('symbol')
        ans += self.writeTag('symbol')
        ans += self.writeTag('statements', self.compileStatements())
        ans += self.writeTag('symbol')

        if self.tokens[self.i] == 'else':
            ans += self.writeTag('keyword')
            ans += self.writeTag('symbol')
            ans += self.writeTag('statements', self.compileStatements())
            ans += self.writeTag('symbol')
        
        return ans


    # whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compileWhileStatement(self):
        ans = ''
        ans += self.writeTag('keyword')
        ans += self.writeTag('symbol')
        ans += self.writeTag('expression', self.compileExpression())
        ans += self.writeTag('symbol')
        ans += self.writeTag('symbol')
        ans += self.writeTag('statements', self.compileStatements())
        ans += self.writeTag('symbol')
        return ans


    # returnStatment: 'return' expression? ';'
    def compileReturnStatement(self):
        ans = ''
        ans += self.writeTag('keyword')
        if self.tokens[self.i] == ';':
            ans += self.writeTag('symbol')
        else:
            ans += self.writeTag('expression', self.compileExpression())
            ans += self.writeTag('symbol')
        return ans


    # varDec: 'var' type varName (',' varName)* ';'
    def compileVarDec(self):
        ans = ''

        # 'var'
        ans += self.writeTag('keyword', 'var')

        # type
        if self.tokens[self.i] in JackType.keywords:
            ans += self.writeTag('keyword')
        else: ans += self.writeTag('identifier')

        # varName
        ans += self.writeTag('identifier')

        # for single variable declaration
        if self.tokens[self.i] == ';':
            ans += self.writeTag('symbol')
            return ans

        # (',' varName)* ';'
        while self.tokens[self.i] != ';':
            if self.tokens[self.i] == ',':
                ans += self.writeTag('symbol')
            else: ans += self.writeTag('identifier')

        ans += self.writeTag('symbol')
        return ans

