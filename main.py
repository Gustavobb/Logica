# macielcalebe
import sys
import re
from enum import Enum

types = ["INT", "PLUS", "SUB", "DIV", "MULT","EOF"]

class Type(Enum):
    INT = 1
    PLUS = 2
    SUB = 3
    DIV = 4
    MULT = 5
    EOF = 6

class Token:

    def __init__(self, type_: Type, value: int):
        self.type_ = type_
        self.value = value

class Tokenizer:

    def __init__(self, origin: str):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.select_next()

    def select_next(self) -> Token:
        token = None
        if self.position == len(self.origin):
            token = Token(Type.EOF, None)
            self.actual = token
            return

        tmp = self.origin[self.position]
    
        if tmp == ' ': 
            while (tmp == ' '):
                self.position += 1

                if self.position == len(self.origin):
                    token = Token(Type.EOF, None)
                    self.actual = token
                    return

                tmp = self.origin[self.position]

        if tmp.isnumeric():
            int_ = ''
            while (True):
                if len(self.origin) > self.position and self.origin[self.position].isnumeric():
                    int_ += self.origin[self.position]
                    self.position += 1
                    continue

                break
        
            self.position -= 1
            token = Token(Type.INT, int(int_))

        elif tmp == '+': 
            token = Token(Type.PLUS, None)

        elif tmp == '-': 
            token = Token(Type.SUB, None)

        elif tmp == '*': 
            token = Token(Type.MULT, None)

        elif tmp == '/': 
            token = Token(Type.DIV, None)

        else:
            raise_error("not found operation")

        self.actual = token
        self.position += 1

class Parser:

    def __init__(self):
        self.tokenizer = None
        self.result = 0
        self.term_value = 0

    def parse_expression(self) -> int:

        if self.tokenizer.actual.type_ == Type.INT:
            self.term()
            self.result = self.term_value
            while (self.tokenizer.actual.type_ != Type.INT and self.tokenizer.actual.type_ != Type.EOF):
                self.apply_operation(Type.PLUS, self.apply_sum)
                self.apply_operation(Type.SUB, self.apply_sub)
            
            return self.result
        
        raise_error("do not start with operators")

    def apply_operation(self, token_type: Type, func) -> int: 
        if self.tokenizer.actual.type_ == token_type:
            self.tokenizer.select_next()
            tmp = self.tokenizer.actual

            if tmp.type_ == Type.INT:
                self.term()
                func()

            else: raise_error("double operators encountered")

    def term(self):
        if self.tokenizer.actual.type_ != Type.EOF:
            self.term_value = self.tokenizer.actual.value
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ == Type.INT: raise_error("double int encountered")

        while (self.tokenizer.actual.type_ == Type.MULT or self.tokenizer.actual.type_ == Type.DIV):
            tmp = self.tokenizer.actual.type_
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.INT:
                if tmp == Type.MULT: self.apply_multiplication() 
                else: self.apply_division()
                self.tokenizer.select_next()

            else: raise_error("double operators encountered")

    def apply_multiplication(self): 
        self.term_value *= self.tokenizer.actual.value

    def apply_division(self): 
        self.term_value = int(self.term_value/self.tokenizer.actual.value)

    def apply_sub(self): 
        self.result -= self.term_value
        self.term_value = 0

    def apply_sum(self): 
        self.result += self.term_value
        self.term_value = 0

    def code(self, code: str) -> int:
        self.tokenizer = Tokenizer(code)
        return self.parse_expression()

class PrePro:

    def filter(self, code: str) -> str:
        comment = False
        final_code = ''
        i = 0

        while (i < len(code)):
            if not comment and i != len(code) - 1 and code[i] == "/" and code[i + 1] == "*": 
                i += 1
                comment = True
                
            elif comment:
                if i == len(code) - 1: raise_error("not closed comment")
                elif code[i] == "*" and code[i + 1] == "/": 
                    comment = False
                    i += 1
    
            else: final_code += code[i]

            i += 1

        return final_code

def raise_error(error: str):
    raise ValueError(error)

def main(argv: str) -> int:
    parser = Parser()
    print(parser.code(PrePro().filter(argv)))
    return 0

if __name__ == "__main__":
    main(sys.argv[1])