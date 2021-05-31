import JackType
import string
import html

class JackTokenizer:
    def __init__(self, infile):

        # current byte infile
        self.seeker = 0
        self.infile = infile

        # current token and its type
        self.current = ''
        self.type = ''

        # store infile to content
        with open(infile, 'r') as file:
            self.content = file.read()

    def hasMoreTokens(self):
        # since we might have whitespace / comments
        # one after the other, we need a flag to check
        # if the last round was a seek due to whitespace
        # or not. If not, we go ahead to parse tokens.
        ws_mod = True
        while ws_mod:
            
            if(self.seeker >= len(self.content)):
                return False
            
            # seek over whitespace
            if self.content[self.seeker] in string.whitespace:
                self.seeker += 1
                continue

            # seek over single-line comments
            if self.content[self.seeker:self.seeker+2] == '//':
                newline = self.content.find('\n', self.seeker+2)
                self.seeker = newline+1
                continue

            # seek over multi-line comments
            if self.content[self.seeker:self.seeker+2] == '/*':
                end_comment = self.content.find('*/', self.seeker+2)
                self.seeker = end_comment+2
                continue
            
            ws_mod = False
        return True
        

    def advance(self):
        # first, parse "symbols". Since they will always
        # be one character long and and easiest to check
        if self.content[self.seeker] in JackType.symbols:
            self.current = html.escape(self.content[self.seeker])
            self.seeker += 1
            self.type = 'symbol'
            return

        # to check for integer constants: iteratively
        # check if character is digit until it isn't
        if self.content[self.seeker].isdigit():
            dig_cnt = 1 # digit counter
            while self.content[self.seeker+dig_cnt].isdigit(): dig_cnt+=1
            self.current = self.content[self.seeker:self.seeker+dig_cnt]
            if int(self.current) > 32767 or int(self.current) < 0:
                print('Integer constant out of range')
                exit()
            self.seeker += dig_cnt
            self.type = 'integerConstant'
            return

        # extract string constants
        if self.content[self.seeker] == '"':
            str_cnt = 1 # string counter
            while self.content[self.seeker+str_cnt] != '"': str_cnt += 1

            # excluding double quotes
            self.current = self.content[self.seeker+1:self.seeker+str_cnt]

            # including double quotes
            #self.current=self.content[self.seeker:self.seeker+str_cnt+1]

            self.seeker += str_cnt+1
            self.type = 'stringConstant'
            return

        # identifiers and keywords can end without a whitespace
        # as an example: if(true) where if is terminated with (
        # another example: arr[0] where arr is terminated with [
        # so we have to check for both whitespace and symbols

        id_kw = 0
        while self.content[self.seeker+id_kw] not in string.whitespace \
          and self.content[self.seeker+id_kw] not in JackType.symbols:
            id_kw += 1

        # it could be an identifier or a keyword
        self.current = self.content[self.seeker:self.seeker+id_kw]
        if self.current in JackType.keywords:
            self.type = 'keyword'
        else: self.type = 'identifier'
        self.seeker += id_kw
        return
