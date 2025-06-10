grammar Arithmetic;

program: statement+ ;
statement: assignment | expr ;
assignment: VAR ASSIGN expr ;
expr: term ( (PLUS | MINUS) term )* ;
term: factor ( (MUL | DIV) factor )* ;
factor: INT | VAR | LPAREN expr RPAREN ;

PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
INT: [0-9]+ ;
VAR: [a-zA-Z]+ ;
ASSIGN: '=' ;
LPAREN: '(' ;
RPAREN: ')' ;
WS: [ \t\r\n]+ -> skip ;