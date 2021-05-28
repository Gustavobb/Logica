# macielcalebe
from enum import Enum
import sys

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
    BOOLDEF = 25
    INTDEF = 26
    STRDEF = 27
    BOOL = 28
    STR = 29

class Token:

    def __init__(self, type_: Type, value: int, id_: int):
        self.type_ = type_
        self.value = value
        self.id_ = id_ 

class Tokenizer:

    def __init__(self, origin: str):
        self.origin = origin
        self.position = 0
        self.actual = None
        self.select_next()

    def select_next(self) -> Token:
        token = None
        if self.position == len(self.origin):
            token = Token(Type.EOF, None, self.position)
            self.actual = token
            return

        tmp = self.origin[self.position]
        
        if tmp == ' ' or tmp == '\n' or tmp == "\t":
            while (tmp == ' ' or tmp == '\n' or tmp == "\t"):
                self.position += 1

                if self.position == len(self.origin):
                    token = Token(Type.EOF, None, self.position)
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
            token = Token(Type.INT, int(int_), self.position)
        
        elif tmp.isalpha() or tmp == '"':
            str_ = ''
            is_str = False

            if tmp == '"': 
                is_str = True
                str_ += '"'
                self.position += 1

            while (True):
                if len(self.origin) > self.position and (self.origin[self.position].isnumeric() or self.origin[self.position].isalpha() or self.origin[self.position] == "_"):
                    str_ += self.origin[self.position]
                    self.position += 1
                    if (self.origin[self.position] == " "):
                        if (is_str): 
                            str_ += self.origin[self.position]
                            self.position += 1
                            continue

                    else: continue

                else:
                    if str_ == "println":
                        token = Token(Type.PRINTLN, None, self.position)
                        break
                    
                    elif str_[0] == '"':
                        str_ += self.origin[self.position]
                        self.position += 1
                        token = Token(Type.STR, str_)
                        break

                    elif str_ == "readln":
                        token = Token(Type.READLN, None, self.position)
                        break
                        
                    elif str_ == "while":
                        token = Token(Type.WHILE, None, self.position)
                        break

                    elif str_ == "if":
                        token = Token(Type.IF, None, self.position)
                        break
                        
                    elif str_ == "else":
                        token = Token(Type.ELSE, None, self.position)
                        break
                
                    elif str_ == "bool":
                        token = Token(Type.BOOLDEF, None, self.position)
                        break
                        
                    elif str_ == "string":
                        token = Token(Type.STRDEF, None, self.position)
                        break
                    
                    elif str_ == "int":
                        token = Token(Type.INTDEF, None, self.position)
                        break
                
                    elif str_ == "true" or str_ == "false":
                        token = Token(Type.BOOL, str_, self.position)
                        break
                        
                    else: 
                        token = Token(Type.IDENTIFIER, str_, self.position)
                        break
            
            self.position -= 1

        elif tmp == "=":
            token = Token(Type.ATR, None, self.position)

            if self.origin[self.position + 1] == "=":
                token = Token(Type.ET, None, self.position)
                self.position += 1
        
        elif tmp == ";":
            token = Token(Type.EOL, None, self.position)

        elif tmp == '+': 
            token = Token(Type.PLUS, 1, self.position)

        elif tmp == '-': 
            token = Token(Type.SUB, -1, self.position)

        elif tmp == '*': 
            token = Token(Type.MULT, None, self.position)

        elif tmp == '/': 
            token = Token(Type.DIV, None, self.position)
        
        elif tmp == ')': 
            token = Token(Type.EPARENTHESIS, None, self.position)
        
        elif tmp == '(': 
            token = Token(Type.SPARENTHESIS, None, self.position)
        
        elif tmp == '>': 
            token = Token(Type.GT, None, self.position)
        
        elif tmp == '<': 
            token = Token(Type.LT, None, self.position)

        elif tmp == '|' and self.origin[self.position + 1] == '|': 
            token = Token(Type.OR, None, self.position)
            self.position += 1
        
        elif tmp == '&' and self.origin[self.position + 1] == '&': 
            token = Token(Type.AND, None, self.position)
            self.position += 1
        
        elif tmp == '!': 
            token = Token(Type.NEG, None, self.position)
        
        elif tmp == '}': 
            token = Token(Type.EKEY, None, self.position)
        
        elif tmp == '{': 
            token = Token(Type.SKEY, None, self.position)

        else:
            raise_error("not found operation")

        self.actual = token
        self.position += 1

class Assembler():

    def __init__(self):
        self.assembly = open("exemplo.txt", "r").read()
    
    def int_val_assembly(self, value: str):
        self.assembly += f"MOV EBX, {value}" + "\n"

    def push_ebx(self):
        self.assembly += "PUSH EBX" + "\n"
    
    def pop_eax(self):
        self.assembly += "POP EAX" + "\n"
    
    def add_operation_assembly(self):
        self.assembly += "ADD EAX, EBX \n MOV EBX, EAX " + "\n"
    
    def sub_operation_assembly(self):
        self.assembly += "SUB EAX, EBX \n MOV EBX, EAX " + "\n"
    
    def mult_operation_assembly(self):
        self.assembly += "IMUL EBX \n MOV EBX, EAX " + "\n"
    
    def div_operation_assembly(self):
        self.assembly += "DIV EAX, EBX \n MOV EBX, EAX " + "\n"
    
    def def_variable(self):
        self.assembly += "PUSH DWORD 0" + "\n"
    
    def atr_variable(self, position: int):
        self.assembly += f"MOV [EBP{position}], EBX" + "\n"
    
    def cmp_assembly(self):
        self.assembly += f"CMP EAX, EBX" + "\n"
    
    def cmp_while_assembly(self, id_: int):
        self.assembly += f"CMP EBX, False \n JE EXIT_{id_}" + "\n"

    def je_assembly(self):
        self.cmp_assembly()
        self.assembly += "CALL binop_je" + "\n"
    
    def jl_assembly(self):
        self.cmp_assembly()
        self.assembly += "CALL binop_jl" + "\n"
    
    def jg_assembly(self):
        self.cmp_assembly()
        self.assembly += "CALL binop_jg" + "\n"
    
    def and_assembly(self):
        self.assembly += "AND EAX, EBX" + "\n"
    
    def or_assembly(self):
        self.assembly += "OR EAX, EBX" + "\n"
    
    def neg_assembly(self):
        self.assembly += "NEG EBX" + "\n"
    
    def not_assembly(self):
        self.assembly += "NOT EBX" + "\n"

    def print_assembly(self):
        self.assembly += "PUSH EBX \n CALL print \n POP EBX" + "\n"

    def while_assembly(self, id_: int):
        self.assembly += f"LOOP_{id_}:" + "\n"

    def if_assembly(self, id_: int):
        self.assembly += f"CMP EBX, True" + "\n"
        self.assembly += f"JE IF_{id_}" + "\n"

    def label_assembly(self, value: str):
        self.assembly += f"{value}:" + "\n"

    def jmp_assembly(self, value: str):
        self.assembly += f"JMP {value}" + "\n"

    def exit_assembly(self, value: str):
        self.assembly += f"EXIT_{value}:" + "\n"
    
    def ident_assembly(self, value: str):
        self.assembly += f"MOV EBX, [EBP{value}]" + "\n"

    def end_assembly(self):
        self.assembly += "POP EBP \n MOV EAX, 1 \n MOV EBX, 0 \n INT 0x80"

class SymbolTable:

    def __init__(self):
        self.dict = {}
        self.pos = -4

    def _get(self, var_name: str) -> int:
        if var_name in self.dict: return self.dict[var_name]["pos"]
        return None

    def _set(self, var_name: str, var_value: int):
        if not var_name in self.dict:
            if var_value != None: raise_error("not initialized var")
            self.dict[var_name] = {}
            self.dict[var_name]["pos"] = self.pos
            self.pos -= 4

class Node:

    def __init__(self, token: Token, n_children: int):
        self.token = token
        self.children = [NoOp() for i in range(n_children)]
        
    def evaluate(self, st: SymbolTable, assembly: Assembler): pass

class BinOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        self.children[0].evaluate(st, assembly)
        assembly.push_ebx()
        self.children[1].evaluate(st, assembly)
        assembly.pop_eax()
        
        if self.token.type_ == Type.PLUS:
            assembly.add_operation_assembly()

        elif self.token.type_ == Type.SUB: 
            assembly.sub_operation_assembly()

        elif self.token.type_ == Type.DIV: 
            assembly.div_operation_assembly()

        elif self.token.type_ == Type.MULT: 
            assembly.mult_operation_assembly()

        elif self.token.type_ == Type.GT:
            assembly.jg_assembly()
 
        elif self.token.type_ == Type.LT: 
            assembly.jl_assembly()

        elif self.token.type_ == Type.ET: 
            assembly.je_assembly()

        elif self.token.type_ == Type.AND: 
            assembly.and_assembly()

        elif self.token.type_ == Type.OR: 
            assembly.or_assembly()

class AtrOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler):
        self.children[1].evaluate(st, assembly)
        st._set(self.children[0].token.value, None)
        r = st._get(self.children[0].token.value)
        assembly.atr_variable(r)

class UnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler):
        self.children[0].evaluate(st, assembly)

        if self.token.type_ == Type.SUB: assembly.neg_assembly()

class NotOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler):
        self.children[0].evaluate(st, assembly)
        assembly.not_assembly()

class PrintOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        self.children[0].evaluate(st, assembly)
        assembly.print_assembly()

class ReadlnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): return int(input()), Type.INT

class IntVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        assembly.int_val_assembly(self.token.value)

class StringVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): return self.token.value[1:-1], self.token.type_

class BoolVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        assembly.int_val_assembly("True" if self.token.value == "true" else "False")

class TypeVal(Node):
    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        if not st._get(self.token.value): 
            st._set(self.children[0].value, None)
            assembly.def_variable()
        else: raise_error("double definition of variable")

class WhileOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler):
        assembly.while_assembly(self.token.id_)
        self.children[0].evaluate(st, assembly)
        assembly.cmp_while_assembly(self.token.id_)
        self.children[1].evaluate(st, assembly)
        assembly.jmp_assembly("LOOP_" + str(self.token.id_))
        assembly.exit_assembly(self.token.id_)

class NoOp(Node):

    def __init__(self):
        super().__init__(None, 0)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): return 

class CondOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 3)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler):
        self.children[0].evaluate(st, assembly)
        assembly.if_assembly(self.token.id_)
        
        if type(self.children[2]) != NoOp:
            self.children[2].evaluate(st, assembly)

        assembly.jmp_assembly("EXIT_" + str(self.token.id_))
        assembly.label_assembly("IF_" + str(self.token.id_))
        self.children[1].evaluate(st, assembly)
        assembly.exit_assembly(self.token.id_)

class IdentVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, st: SymbolTable, assembly: Assembler): 
        r = st._get(self.token.value)
        if not r: raise_error("key not found")
        
        assembly.ident_assembly(r)

class Block():
    def __init__(self, tree: list):
        self.tree = tree

    def evaluate(self, st: SymbolTable, assembly: Assembler):
        for tree in self.tree: 
            tree.evaluate(st, assembly)

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
        
        elif self.tokenizer.actual.type_ == Type.BOOL:
            node = BoolVal(self.tokenizer.actual)
            self.tokenizer.select_next()
            return node
        
        elif self.tokenizer.actual.type_ == Type.STR:
            node = StringVal(self.tokenizer.actual)
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

        elif self.tokenizer.actual.type_ in [Type.BOOLDEF, Type.INTDEF, Type.STRDEF]:
            node = TypeVal(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.IDENTIFIER: raise_error("wrong definition of variable")
            node.children[0] = self.tokenizer.actual
            self.tokenizer.select_next()
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
    
    assembly = Assembler()
    st = SymbolTable()
    trees.evaluate(st, assembly)
    assembly.end_assembly()

    print(assembly.assembly)
    return 0

if __name__ == "__main__":
    main(sys.argv[1])