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
    SPARENTESIS = 6
    EPARENTESIS = 7
    EOF = 8

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
        
        elif tmp == ')': 
            token = Token(Type.EPARENTESIS, None)
        
        elif tmp == '(': 
            token = Token(Type.SPARENTESIS, None)

        else:
            raise_error("not found operation")

        self.actual = token
        self.position += 1

class Parser:

    def __init__(self):
        self.tokenizer = None

    def parse_expression(self) -> int:
        result = self.term()

        while (self.tokenizer.actual.type_ == Type.PLUS or self.tokenizer.actual.type_ == Type.SUB):
            result = self.apply_operation(Type.PLUS, self.apply_sum, result)
            result = self.apply_operation(Type.SUB, self.apply_sub, result)
            
        return result

    def apply_operation(self, token_type: Type, func, result: int) -> int:
        if self.tokenizer.actual.type_ == token_type:
            self.tokenizer.select_next()
            return func(result)
        
        return result

    def factor(self):
        if self.tokenizer.actual.type_ == Type.INT:
            tmp = self.tokenizer.actual.value
            self.tokenizer.select_next()
            return tmp

        elif self.tokenizer.actual.type_ == Type.PLUS:
            self.tokenizer.select_next()
            return self.factor()
            
        elif self.tokenizer.actual.type_ == Type.SUB:
            self.tokenizer.select_next()
            return -self.factor()
        
        elif self.tokenizer.actual.type_ == Type.SPARENTESIS:
            self.tokenizer.select_next()
            result_tmp = self.parse_expression()

            if self.tokenizer.actual.type_ == Type.EPARENTESIS: 
                self.tokenizer.select_next()
                return result_tmp

            else: raise_error("parentesis not closed")

    def term(self):
        term_value = self.factor()
        if self.tokenizer.actual.type_ == Type.INT: raise_error("double int encountered")

        while (self.tokenizer.actual.type_ == Type.MULT or self.tokenizer.actual.type_ == Type.DIV):
            tmp = self.tokenizer.actual.type_
            self.tokenizer.select_next()
            
            if self.tokenizer.actual.type_ == Type.MULT or self.tokenizer.actual.type_ == Type.DIV: 
                raise_error("double operation encountered")
            
            if tmp == Type.MULT: term_value = self.apply_multiplication(term_value) 
            else: term_value = self.apply_division(term_value)

        return term_value

    def apply_multiplication(self, term_value: int): 
        return term_value * self.factor()

    def apply_division(self, term_value: int): 
        return int(term_value/self.factor())

    def apply_sub(self, result: int):
        return result - self.term()

    def apply_sum(self, result: int): 
        return result + self.term()

    def code(self, code: str) -> int:
        self.tokenizer = Tokenizer(code)
        result = self.parse_expression()
        if self.tokenizer.actual.type_ != Type.EOF: raise_error("not initialized parentesis")
        return result

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