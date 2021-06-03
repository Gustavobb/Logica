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
    RETURN = 30
    COMMA = 31

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
        
        if tmp == ' ' or tmp == '\n' or tmp == "\t":
            while (tmp == ' ' or tmp == '\n' or tmp == "\t"):
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
                        token = Token(Type.PRINTLN, None)
                        break
                    
                    elif str_[0] == '"':
                        str_ += self.origin[self.position]
                        self.position += 1
                        token = Token(Type.STR, str_)
                        break

                    elif str_ == "readln":
                        token = Token(Type.READLN, None)
                        break
                    
                    elif str_ == "return":
                        token = Token(Type.RETURN, None)
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
                
                    elif str_ == "bool":
                        token = Token(Type.BOOLDEF, None)
                        break
                        
                    elif str_ == "string":
                        token = Token(Type.STRDEF, None)
                        break
                    
                    elif str_ == "int":
                        token = Token(Type.INTDEF, None)
                        break
                
                    elif str_ == "true" or str_ == "false":
                        token = Token(Type.BOOL, str_)
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

        elif tmp == ',': 
            token = Token(Type.COMMA, -1)

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

class FunctionSymbolTable:

    def __init__(self):
        self.dict = {}

    def create_function(self, func_name: str, func_type: Type, func):
        if func_name not in self.dict:
            self.dict[func_name] = {}
            self.dict[func_name]["node"] = func
            self.dict[func_name]["type"] = func_type
            return True

        return False
    
    def _get_variable(self, var_name: str, func_name: str) -> int:
        if var_name in self.dict[func_name]: 
            return True

        return False

    def _set_variable(self, var_name: str, var_value: int, var_type: Type, func_name: str, var_func_type="local"):
        if not var_name in self.dict[func_name]:
            if var_value != None: raise_error("not initialized var")
            self.dict[func_name][var_name] = {}
            self.dict[func_name][var_name]["type"] = var_type
            self.dict[func_name][var_name]["var_func_type"] = var_func_type
        
        else:
            raise_error("double def in arguments")

class SymbolTable:

    def __init__(self, f: dict):
        self.dict = f.copy()

    def _get_variable(self, var_name: str, func_name: str) -> int:
        if var_name in self.dict:
            try: return self.dict[var_name]["value"], self.dict[var_name]["type"]
            except: return True

        return None
    
    def _get_node(self):
        if self.dict["node"] != None: 
            return self.dict["node"]
            
        return None

    def _set_variable(self, var_name: str, var_value: int, var_type: Type, func_name: str, var_func_type="local"):
        if not var_name in self.dict:
            if var_value != None: raise_error("not initialized var")
            self.dict[var_name] = {}
            self.dict[var_name]["type"] = var_type
            self.dict[var_name]["var_func_type"] = var_func_type
        
        else:
            if self.dict[var_name]["type"] != var_type: 
                if var_type == Type.STR or self.dict[var_name]["type"] == Type.STR: raise_error("not compatible types")

                if var_type == Type.BOOL: var_value = int(var_value)
                elif var_type == Type.INT: var_value = bool(var_value)

            self.dict[var_name]["value"] = var_value

class Node:

    def __init__(self, token: Token, n_children: int):
        self.token = token
        self.children = [NoOp() for i in range(n_children)]
        
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): pass

class BinOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        eval1 = self.children[0].evaluate(fst, st, func_name)
        eval2 = self.children[1].evaluate(fst, st, func_name)

        if (eval1[1] == Type.STR or eval2[1] == Type.STR) and self.token.type_ != Type.ET: raise_error("incompatible types")

        if self.token.type_ == Type.PLUS: 
            return eval1[0] + eval2[0], Type.INT

        elif self.token.type_ == Type.SUB: 
            return eval1[0] - eval2[0], Type.INT

        elif self.token.type_ == Type.DIV: 
            return int(eval1[0] / eval2[0]), Type.INT

        elif self.token.type_ == Type.MULT: 
            return int(eval1[0] * eval2[0]), Type.INT

        elif self.token.type_ == Type.GT:
            return bool(eval1[0] > eval2[0]), Type.BOOL
 
        elif self.token.type_ == Type.LT: 
            return bool(eval1[0] < eval2[0]), Type.BOOL

        elif self.token.type_ == Type.ET: 
            return bool(eval1[0] == eval2[0]), Type.BOOL

        elif self.token.type_ == Type.AND: 
            return bool(eval1[0] and eval2[0]), Type.BOOL

        elif self.token.type_ == Type.OR: 
            return bool(eval1[0] or eval2[0]), Type.BOOL

class AtrOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        node = self.children[1].evaluate(fst, st, func_name)
        st._set_variable(self.children[0].token.value, node[0], node[1], func_name)

class UnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        node = self.children[0].evaluate(fst, st, func_name)
        return self.token.value * node[0], node[1]

class NotOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        node = self.children[0].evaluate(fst, st, func_name)
        return not node[0], node[1] 

class PrintOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        node = self.children[0].evaluate(fst, st, func_name)
        p = node[0]
        if node[1] == Type.BOOL: p = "true" if node[0] else "false"
        print(p)

class ReadlnOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): return int(input()), Type.INT

class IntVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): return self.token.value, self.token.type_

class StringVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): return self.token.value[1:-1], self.token.type_

class BoolVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): return True if self.token.value == "true" else False, self.token.type_

class VarDec(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        for i in self.children: i.evaluate(fst, st, func_name)

class FuncDec(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str):
        if not fst.create_function(self.token.value, self.token.type_, self): raise_error("multiple declaration of same function")
        self.children[0].evaluate(fst, st, self.token.value)

class ReturnVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 1)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        return self.children[0].evaluate(fst, st, func_name)

class FuncCall(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str):
        st_ = SymbolTable(fst.dict[self.token.value])
        node = st_._get_node()
        if not node: raise_error("func not defined")
        
        l = []
        for key in st_.dict.items():
            if type(key[1]) is dict:
                if key[1]["var_func_type"] == "argument": l += [(key[0], key[1]["type"])]
        
        if len(l) != len(self.children): raise_error("different sizes in call, def function")

        for i in range(len(self.children)):
            # mudar st
            value = self.children[i].evaluate(fst, st, func_name)
            if (value[1] != l[i][1]): raise_error("invalid type in function call")
            st_._set_variable(l[i][0], value[0], value[1], self.token.value)
        
        return_ = node.children[1].evaluate(fst, st_, self.token.value);
        
        if (return_ == None): return
        if st_.dict["type"] == Type.INTDEF: type_ = Type.INT
        elif st_.dict["type"] == Type.STRDEF: type_ = Type.STR
        elif st_.dict["type"] == Type.BOOLDEF: type_ = Type.BOOL
        
        if (return_[1] != type_): raise_error("invalid return type")
        return return_

class TypeVal(Node):

    def __init__(self, token: Token, var_func_type: str):
        super().__init__(token, 1)
        self.var_func_type = var_func_type
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        if self.token.type_ == Type.INTDEF: type_ = Type.INT
        elif self.token.type_ == Type.STRDEF: type_ = Type.STR
        elif self.token.type_ == Type.BOOLDEF: type_ = Type.BOOL

        if self.var_func_type == "local":
            if not st._get_variable(self.children[0].value, func_name): st._set_variable(self.children[0].value, None, type_, func_name, self.var_func_type)
            else: raise_error("double definition of variable(s)")

        else:
            if not fst._get_variable(self.children[0].value, func_name): fst._set_variable(self.children[0].value, None, type_, func_name, self.var_func_type)
            else: raise_error("double definition of variable")

class WhileOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 2)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        while(self.children[0].evaluate(fst, st, func_name)[0]): 
            self.children[1].evaluate(fst, st, func_name)

class CondOp(Node):

    def __init__(self, token: Token):
        super().__init__(token, 3)
            
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): 
        cond = self.children[0].evaluate(fst, st, func_name)[0]
        if type(cond) is str: raise_error("cant have str in if")
        if cond: return self.children[1].evaluate(fst, st, func_name)

        if type(self.children[2]) != NoOp:
            if not cond: return self.children[2].evaluate(fst, st, func_name)

class IdentVal(Node):

    def __init__(self, token: Token):
        super().__init__(token, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str):
        r = st._get_variable(self.token.value, func_name)
        if not r: raise_error("key not found")
        return r

class NoOp(Node):

    def __init__(self):
        super().__init__(None, 0)
    
    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str): return 

class Block():
    
    def __init__(self, tree: list):
        self.tree = tree

    def evaluate(self, fst: FunctionSymbolTable, st: SymbolTable, func_name: str):
        for tree in self.tree:
            r = tree.evaluate(fst, st, func_name)
            if r != None and not isinstance(tree, FuncCall):
                return r

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
            token = self.tokenizer.actual
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.SPARENTHESIS:
                node = FuncCall(token)

                comma = False
                while (self.tokenizer.actual.type_ != Type.EPARENTHESIS):
                    self.tokenizer.select_next()
                    result = self.orexpr()
                    if result != None: node.children.append(result)
                    elif comma: raise_error("expecting new argument")

                    if self.tokenizer.actual.type_ == Type.COMMA: 
                        comma = True
                        continue

                    elif self.tokenizer.actual.type_ != Type.EPARENTHESIS: raise_error("wrong definition of function arguments")
                
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
            token = self.tokenizer.actual
            self.tokenizer.select_next()

            if self.tokenizer.actual.type_ == Type.SPARENTHESIS:
                node = FuncCall(token)

                comma = False
                while (self.tokenizer.actual.type_ != Type.EPARENTHESIS):
                    self.tokenizer.select_next()
                    result = self.orexpr()
                    
                    if result != None: 
                        comma = False
                        node.children.append(result)

                    elif comma: raise_error("expecting new argument")

                    if self.tokenizer.actual.type_ == Type.COMMA: 
                        comma = True
                        continue

                    elif self.tokenizer.actual.type_ != Type.EPARENTHESIS: raise_error("wrong definition of function arguments")
                
                self.tokenizer.select_next()
            
            elif self.tokenizer.actual.type_ == Type.ATR:
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
            node = TypeVal(self.tokenizer.actual, "local")
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ != Type.IDENTIFIER: raise_error("wrong definition of variable")
            node.children[0] = self.tokenizer.actual
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ == Type.EOL: self.tokenizer.select_next()
            else: raise_error("not closed sintax")
            return node
        
        elif self.tokenizer.actual.type_ == Type.RETURN:
            node = ReturnVal(self.tokenizer.actual)
            self.tokenizer.select_next()
            if self.tokenizer.actual.type_ not in [Type.INT, Type.STR, Type.BOOL, Type.IDENTIFIER]: raise_error("return is a reserved word")
            node.children[0] = self.orexpr()
            if self.tokenizer.actual.type_ != Type.EOL: raise_error("not closed sintax")
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
    
    def func_def_block(self):
        ast = []

        while (self.tokenizer.actual.type_ != Type.EOF):
            if self.tokenizer.actual.type_ in [Type.BOOLDEF, Type.INTDEF, Type.STRDEF]:

                # name and type
                node = FuncDec(self.tokenizer.actual)
                self.tokenizer.select_next()
                if self.tokenizer.actual.type_ != Type.IDENTIFIER: raise_error("wrong definition of function")
                node.token.value = self.tokenizer.actual.value

                # arguments
                self.tokenizer.select_next()
                if self.tokenizer.actual.type_ != Type.SPARENTHESIS: raise_error("wrong definition of function")
                self.tokenizer.select_next()
                node_child_0 = VarDec(self.tokenizer.actual.type_)
                
                comma = False
                while (self.tokenizer.actual.type_ != Type.EPARENTHESIS):

                    if self.tokenizer.actual.type_ in [Type.BOOLDEF, Type.INTDEF, Type.STRDEF]:
                        type_node = TypeVal(self.tokenizer.actual, "argument")
                        self.tokenizer.select_next()
                        if self.tokenizer.actual.type_ != Type.IDENTIFIER: raise_error("wrong definition of arguments")
                        type_node.children[0] = self.tokenizer.actual
                        self.tokenizer.select_next()
                        
                        if self.tokenizer.actual.type_ != Type.COMMA and self.tokenizer.actual.type_ != Type.EPARENTHESIS: raise_error("wrong definition of arguments")
                        
                        node_child_0.children.append(type_node)
                        continue
                    
                    if self.tokenizer.actual.type_ == Type.COMMA: comma = True
                    self.tokenizer.select_next()
                    if comma and self.tokenizer.actual.type_ not in [Type.BOOLDEF, Type.INTDEF, Type.STRDEF]: raise_error("expected new argument")
                
                node.children[0] = node_child_0
                self.tokenizer.select_next()

                # stm
                node.children[1] = self.command()
                ast += [node]
            
            else: raise_error("sintax error")
        
        return ast

    def code(self, code: str) -> int:
        self.tokenizer = Tokenizer(code)
        ast = self.func_def_block()
        ast.append(FuncCall(Token(None, "main")))
        return ast

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
    fst = FunctionSymbolTable()

    for tree in trees:
        tree.evaluate(fst, None, None)

    return 0

if __name__ == "__main__":
    main(sys.argv[1])