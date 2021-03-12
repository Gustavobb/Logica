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

    def parse_expression(self) -> int:

        if self.tokenizer.actual.type_ == Type.INT:
            self.result = self.tokenizer.actual.value
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.INT: raise_error("double int encountered")
            
            while (self.tokenizer.actual.type_ == Type.PLUS or self.tokenizer.actual.type_ == Type.SUB or 
            self.tokenizer.actual.type_ == Type.DIV or self.tokenizer.actual.type_ == Type.MULT):
                self.apply_operation(Type.PLUS, self.apply_sum)
                self.apply_operation(Type.SUB, self.apply_sub)
                self.apply_operation(Type.DIV, self.apply_division)
                self.apply_operation(Type.MULT, self.apply_multiplication)

                if self.tokenizer.actual.type_ != Type.EOF:
                    self.tokenizer.select_next()
                    
                    if self.tokenizer.actual.type_ == Type.INT: raise_error("double int encountered")
            
            return self.result
        
        raise_error("do not start with operators")

    def apply_operation(self, token_type: Type, func) -> int: 
        if self.tokenizer.actual.type_ == token_type:
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.INT:
                func()

            else:
                raise_error("double operators encountered")

    def apply_multiplication(self): 
        self.result *= self.tokenizer.actual.value

    def apply_division(self): 
        self.result /= self.tokenizer.actual.value

    def apply_sub(self): 
        self.result -= self.tokenizer.actual.value

    def apply_sum(self): 
        self.result += self.tokenizer.actual.value 

    def code(self, code: str) -> int:
        self.tokenizer = Tokenizer(code)
        return self.parse_expression()

def raise_error(error: str):
    raise ValueError(error)

def main(argv: str) -> int:
    parser = Parser()
    print(parser.code(argv))
    return 0

if __name__ == "__main__":
    main(sys.argv[1])