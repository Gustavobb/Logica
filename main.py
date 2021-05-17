# macielcalebe
from enum import Enum
import sys

types = ["INT", "PLUS", "SUB", "DIV", "MULT", "EOF"]

class Type(Enum):

    INT = 1
    PLUS = 2
    SUB = 3
    DIV = 4
    MULT = 5
    SPARENTHESIS = 6
    EPARENTHESIS = 7
    EOF = 8
    EOL = 9
    ATR = 10
    PRINTLN = 11
    IDENTIFIER = 12
    READLN = 13
    GT = 14
    LT = 15
    ET = 16
    OR = 17
    AND = 18
    NEG = 19
    IF = 20
    ELSE = 21
    WHILE = 22
    SKEY = 23
    EKEY = 24

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

        if tmp == ' ' or tmp == '\n': 
            while (tmp == ' ' or tmp == '\n'):
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
        
        elif tmp.isalpha():
            str_ = ''
            while (True):
                if len(self.origin) > self.position and (self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_"):
                    str_ += self.origin[self.position]
                    self.position += 1
                    continue
                
                else:
                    if str_ == "println":
                        token = Token(Type.PRINTLN, None)
                        break
                    
                    elif str_ == "readln":
                        token = Token(Type.READLN, None)
                        break
                        
                    elif str_ == "while":
                        token = Token(Type.WHILE, None)
                        break

                    elif str_ == "if":
                        token = Token(Type.IF, None)
                        break
                        
                    elif str_ == "else":
                        token = Token(Type.ELSE, None)
                        break
                        
                    else: 
                        token = Token(Type.IDENTIFIER, str_)
                        break
            
            self.position -= 1

        elif tmp == "=":
            token = Token(Type.ATR, None)

            if self.origin[self.position + 1] == "=":
                token = Token(Type.ET, None)
                self.position += 1
        
        elif tmp == ";":
            token = Token(Type.EOL, None)

        elif tmp == '+': 
            token = Token(Type.PLUS, 1)

        elif tmp == '-': 
            token = Token(Type.SUB, -1)

        elif tmp == '*': 
            token = Token(Type.MULT, None)

        elif tmp == '/': 
            token = Token(Type.DIV, None)
        
        elif tmp == ')': 
            token = Token(Type.EPARENTHESIS, None)
        
        elif tmp == '(': 
            token = Token(Type.SPARENTHESIS, None)
        
        elif tmp == '>': 
            token = Token(Type.GT, None)
        
        elif tmp == '<': 
            token = Token(Type.LT, None)

        elif tmp == '|' and self.origin[self.position + 1] == '|': 
            token = Token(Type.OR, None)
            self.position += 1
        
        elif tmp == '&' and self.origin[self.position + 1] == '&': 
            token = Token(Type.AND, None)
            self.position += 1
        
        elif tmp == '!': 
            token = Token(Type.NEG, None)
        
        elif tmp == '}': 
            token = Token(Type.EKEY, None)
        
        elif tmp == '{': 
            token = Token(Type.SKEY, None)

        else:
            raise_error("not found operation")

        self.actual = token
        self.position += 1

class SymbolTable:

    def __init__(self):
        self.dict = {}

    def _get(self, var_name: str) -> int:
        if var_name in self.dict: return self.dict[var_name]
        raise_error("key not found")

    def _set(self, var_name: str, var_value: int):
        self.dict[var_name] = var_value

class Node:

    def __init__(self, token: Token, n_children: int):
        self.token = token
        self.children = [NoOp() for i in range(n_children)]
        
    def evaluate(self, st: SymbolTable): pass

class BinOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable): 
        r = 0
        if self.token.type_ == Type.PLUS: 
            r = self.children[0].evaluate(st) + self.children[1].evaluate(st)
        elif self.token.type_ == Type.SUB: 
            r = self.children[0].evaluate(st) - self.children[1].evaluate(st)
        elif self.token.type_ == Type.DIV: 
            r = int(self.children[0].evaluate(st) / self.children[1].evaluate(st))
        elif self.token.type_ == Type.MULT: 
            r = int(self.children[0].evaluate(st) * self.children[1].evaluate(st))
        elif self.token.type_ == Type.GT: 
            r = self.children[0].evaluate(st) > self.children[1].evaluate(st)
        elif self.token.type_ == Type.LT: 
            r = self.children[0].evaluate(st) < self.children[1].evaluate(st)
        elif self.token.type_ == Type.ET: 
            r = self.children[0].evaluate(st) == self.children[1].evaluate(st)
        elif self.token.type_ == Type.AND: 
            r = self.children[0].evaluate(st) and self.children[1].evaluate(st)
        elif self.token.type_ == Type.OR: 
            r = self.children[0].evaluate(st) or self.children[1].evaluate(st)

        return r

class AtrOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable): 
        st._set(self.children[0].token.value, self.children[1].evaluate(st))

class UnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable): return self.token.value * self.children[0].evaluate(st)

class NotOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable): return not self.children[0].evaluate(st)

class PrintOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable): print(self.children[0].evaluate(st))

class ReadlnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable): return int(input())

class IntVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable): return self.token.value

class WhileOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable): 
        while(self.children[0].evaluate(st)): self.children[1].evaluate(st)

class CondOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 3)
    
    def evaluate(self, st: SymbolTable): 
        cond = self.children[0].evaluate(st)
        if cond: self.children[1].evaluate(st)
        if self.children[2] != None:
            if not cond: self.children[2].evaluate(st)


class IdentVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable): return st._get(self.token.value)

class NoOp(Node):

    def __init__(self):
        super().__init__(None, 0)
    
    def evaluate(self, st: SymbolTable): return 

class Block():
    def __init__(self, tree: list):
        self.tree = tree

    def evaluate(self, st: SymbolTable):
        for tree in self.tree: 
            tree.evaluate(st)

class Parser:

    def __init__(self):
        self.tokenizer = None

    def parse_expression(self) -> int:
        tree = self.term()

        while (self.tokenizer.actual.type_ == Type.PLUS or self.tokenizer.actual.type_ == Type.SUB):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()
            tree.children[1] = self.term()
        
        return tree

    def factor(self) -> Node:
        if self.tokenizer.actual.type_ == Type.INT:
            node = IntVal(self.tokenizer.actual)
            self.tokenizer.select_next()
            return node

        elif self.tokenizer.actual.type_ == Type.PLUS or self.tokenizer.actual.type_ == Type.SUB:
            node = UnOp(self.tokenizer.actual)
            self.tokenizer.select_next() 
            node.children[0] = self.factor()
            return node
        
        elif self.tokenizer.actual.type_ == Type.NEG:
            node = NotOp(self.tokenizer.actual)
            self.tokenizer.select_next() 
            node.children[0] = self.factor()
            return node

        elif self.tokenizer.actual.type_ == Type.IDENTIFIER:
            node = IdentVal(self.tokenizer.actual)
            self.tokenizer.select_next()
            return node

        elif self.tokenizer.actual.type_ == Type.READLN:
            node = ReadlnOp(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.SPARENTHESIS: raise_error("readln is a reserved word")
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.EPARENTHESIS: raise_error("not closed parenthesis")
            self.tokenizer.select_next()
            return node
        
        elif self.tokenizer.actual.type_ == Type.SPARENTHESIS:
            self.tokenizer.select_next()
            tree = self.orexpr()

            if self.tokenizer.actual.type_ == Type.EPARENTHESIS: 
                self.tokenizer.select_next()
                return tree

            else: raise_error("parenthesis not closed")

    def term(self):
        tree = self.factor()
        if self.tokenizer.actual.type_ == Type.INT: raise_error("double int encountered")
        
        while (self.tokenizer.actual.type_ == Type.MULT or self.tokenizer.actual.type_ == Type.DIV):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()
            
            if self.tokenizer.actual.type_ == Type.MULT or self.tokenizer.actual.type_ == Type.DIV: 
                raise_error("double operation encountered")
            
            tree.children[1] = self.factor()

        return tree
    
    def relexpr(self):
        tree = self.parse_expression()

        if (self.tokenizer.actual.type_ == Type.GT or self.tokenizer.actual.type_ == Type.LT):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()
            if (self.tokenizer.actual.type_ == Type.GT or self.tokenizer.actual.type_ == Type.LT): raise_error("double relexpr")
            tree.children[1] = self.parse_expression()
            
            while (self.tokenizer.actual.type_ == Type.GT or self.tokenizer.actual.type_ == Type.LT):
                tmp2 = tree
                tree = BinOp(self.tokenizer.actual)
                tree.children[0] = tmp2
                self.tokenizer.select_next()
                tree.children[1] = self.parse_expression()

        return tree

    def eqexpr(self):
        tree = self.relexpr()

        if (self.tokenizer.actual.type_ == Type.ET):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()

            if (self.tokenizer.actual.type_ == Type.ET): raise_error("double eqexpr")
            tree.children[1] = self.relexpr()

            while (self.tokenizer.actual.type_ == Type.ET):
                tmp2 = tree
                tree = BinOp(self.tokenizer.actual)
                tree.children[0] = tmp2
                self.tokenizer.select_next()
                tree.children[1] = self.relexpr()
        
        return tree

    def andexpr(self):
        tree = self.eqexpr()

        if (self.tokenizer.actual.type_ == Type.AND):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()

            if (self.tokenizer.actual.type_ == Type.AND): raise_error("double and")
            tree.children[1] = self.eqexpr()

            while (self.tokenizer.actual.type_ == Type.AND):
                tmp2 = tree
                tree = BinOp(self.tokenizer.actual)
                tree.children[0] = tmp2
                self.tokenizer.select_next()
                tree.children[1] = self.eqexpr()
        
        return tree

    def orexpr(self):
        tree = self.andexpr()

        if (self.tokenizer.actual.type_ == Type.OR):
            tmp = tree
            tree = BinOp(self.tokenizer.actual)
            tree.children[0] = tmp
            self.tokenizer.select_next()

            if (self.tokenizer.actual.type_ == Type.OR): raise_error("double orexpr")
            tree.children[1] = self.andexpr()

            while (self.tokenizer.actual.type_ == Type.OR):
                tmp2 = tree
                tree = BinOp(self.tokenizer.actual)
                tree.children[0] = tmp2
                self.tokenizer.select_next()
                tree.children[1] = self.andexpr()

        return tree
    
    def command(self):
        if self.tokenizer.actual.type_ == Type.IDENTIFIER:
            node = IdentVal(self.tokenizer.actual)
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.ATR:
                tmp = node
                node = AtrOp(self.tokenizer.actual)
                node.children[0] = tmp
                self.tokenizer.select_next()
                node.children[1] = self.orexpr()   

            if self.tokenizer.actual.type_ == Type.INT: raise_error("operator not found")
            if self.tokenizer.actual.type_ == Type.EOL: self.tokenizer.select_next()
            else: raise_error("not closed sintax")

            return node
        
        elif self.tokenizer.actual.type_ == Type.PRINTLN:
            node = PrintOp(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.SPARENTHESIS: raise_error("println is a reserved word")
            node.children[0] = self.orexpr()
            if self.tokenizer.actual.type_ == Type.EOL: self.tokenizer.select_next()
            else: raise_error("not closed sintax")
            return node

        elif self.tokenizer.actual.type_ == Type.SKEY: 
            return self.block()
        
        elif self.tokenizer.actual.type_ == Type.WHILE:
            node = WhileOp(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.SPARENTHESIS: raise_error("while is a reserved word")
            node.children[0] = self.orexpr()  
            node.children[1] = self.command()
            return node
        
        elif self.tokenizer.actual.type_ == Type.IF:
            node = CondOp(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.SPARENTHESIS: raise_error("if is a reserved word")
            node.children[0] = self.orexpr()
            node.children[1] = self.command()
            
            if self.tokenizer.actual.type_ == Type.ELSE:      
                self.tokenizer.select_next()     
                node.children[2] = self.command()
                                    
            return node
    
        elif self.tokenizer.actual.type_ == Type.EOL: 
            self.tokenizer.select_next()

        else: 
            # print(self.tokenizer.actual.type_)
            raise_error("not closed sintax")

    def block(self):
        trees = []
        if not self.tokenizer.actual.type_ == Type.SKEY: raise_error("not initialized keys")
        self.tokenizer.select_next()
        while (self.tokenizer.actual.type_ != Type.EKEY and self.tokenizer.actual.type_ != Type.EOF):
            node = self.command()
            if not node: node = NoOp()
            trees += [node]
        
        if self.tokenizer.actual.type_ == Type.EKEY: self.tokenizer.select_next()
        
        return Block(trees)

    def code(self, code: str) -> int:
        self.tokenizer = Tokenizer(code)
        return self.block()

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
    trees = Parser().code(PrePro().filter(open(argv, "r").read()))
    st = SymbolTable()
    trees.evaluate(st)
    return 0

if __name__ == "__main__":
    main(sys.argv[1])