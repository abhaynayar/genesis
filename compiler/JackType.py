# symbols
symbols = ['{','}','(',')','[',']','.',',',';','+','^',
            '-','*','/','&',',','<','>','=','~','|']

# keywords
keywords = ['class','constructor','function',
            'method','field','static','var','int',
            'char','boolean','void','true','false',
            'null','this','let','do','if','else',
            'while','return']

# classvars
classvars = ['static', 'field']

# subroutines
subroutines = ['constructor', 'function', 'method']

# statements
statements = ['let', 'if', 'while', 'do', 'return']

# operators
operators = ['+','-','*','/','&','|','<','>','=','^']
op_vm = {
    '+': 'add',
    '-': 'sub',
    '|': 'or',
    '=': 'eq',
    # '*': 'call Math.multiply 2',
    # '/': 'call Math.divide 2',
    '*': 'mul',
    '/': 'div',
    '^': 'xor',
    '&gt;': 'gt',
    '&lt;': 'lt',
    '&amp;': 'and',
}

# types for paramlist
types = ['int','char','boolean']

# unary operations
unary = ['-','~']
unary_vm = {
    '-': 'neg',
    '~': 'not'
}

# kind to segment mapping
kindSegment = {
    'VAR': 'local',
    'ARG': 'argument',
    'STATIC': 'static',
    'FIELD': 'this'
}
