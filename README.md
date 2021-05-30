# Logica

Basta rodar python3 main.py <string da operacao>
 
Exemplo: python3 main.py "2+2"

# Status dos testes
![git status](http://3.129.230.99/svg/Gustavobb/Logica/)

# EBNF: 

FUNCDEFBLOCK = TYPE, IDENTIFIER, "(", (TYPE, IDENTIFIER | ,), ")", COMMAND

BLOCK = "{", { COMMAND }, "}" ; 

COMMAND = ( λ | ASSIGNMENT | PRINT | BLOCK | WHILE | IF | STRDEF | BOOLDEF | INTDEF | (IDENTIFIER | IDENTIFIER, "(", (OREXPR | ,), ")")), ";" ; 

WHILE = "while", "(", OREXPR ,")", COMMAND;

IF = "if", "(", OREXPR ,")", COMMAND, (("else", COMMAND) | λ );

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ; 

PRINT = "println", "(", OREXPR, ")" ; 

OREXPR = ANDEXPR, { "||", ANDEXPR } ;

ANDEXPR = EQEXPR, { "&&", EQEXPR } ;

EQEXPR = RELEXPR, { "==", RELEXPR } ;

RELEXPR = EXPRESSION, { (">"|"<"),  EXPRESSION }

EXPRESSION = TERM, { ("+" | "-"), TERM } ; 

TERM = FACTOR, { ("*" | "/"), FACTOR } ; 

FACTOR = (("+" | "-" | "!" ), FACTOR) | NUMBER | BOOL | STR | "(", OREXPR,  ")" | IDENTIFIER | (IDENTIFIER, "(", (OREXPR | ,), ")") | READLN;

READLN = "readln", "(",")";

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ; 

INTDEF = int, IDENTIFIER ;
BOOLDEF = bool, IDENTIFIER ;
STRDEF = str, IDENTIFIER ;

NUMBER = DIGIT, { DIGIT } ; 
BOOL = true | false ; 
STR = " , LETTER | DIGIT, " ; 
LETTER = ( a | ... | z | A | ... | Z ) ; 
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
