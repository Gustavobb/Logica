# Logica

Basta rodar python3 main.py <string da operacao>
 
Exemplo: python3 main.py "2+2"

EBNF: 

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION,")" | number ;

