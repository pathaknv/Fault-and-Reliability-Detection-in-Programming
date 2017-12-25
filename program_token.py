from ply import lex as _lex
from ply import yacc as _yacc

tokens = ['NUMBER','PLUS','MINUS','MULT','DIVIDE','LPAREN','RPAREN','ID','COMMA',
        'SEMICOLON', 'LEFTBRACE', 'RIGHTBRACE','ASSIGN','EQUAL','LESS', 'GREATER']

reserved={
    'while' : 'WHILE', 'else' : 'ELSE', 'if' : 'IF', 'for' : 'FOR', 'switch':'SWITCH',
    'case':'CASE', 'do' : 'DO', 'break': 'BREAK', 'return' : 'RETURN', 'int' : 'INT',
    'float' : 'FLOAT', 'double' : 'DOUBLE', 'continue' : 'CONTINUE', 'struct' : 'STRUCT',
    'union' : 'UNION', 'char' : 'CHAR', 'printf':'PRINTF', 'scanf' : 'SCANF',
}
tokens += reserved.values()

t_CONTINUE = r'continue'
t_CASE = r'case'
t_ELSE = r'else'
t_BREAK = r'break'
t_INT = r'int'
t_SCANF = r'scanf'
t_UNION = r'union'
t_PRINTF = r'printf'
t_CHAR = r'char'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_LEFTBRACE = r'{'
t_RIGHTBRACE = r'}'
t_PLUS = r'\+'
t_MINUS   = r'-'
t_MULT   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_FOR = r'for'
t_WHILE = r'while'
t_SWITCH = r'switch'
t_STRUCT = r'struct'
t_RETURN = r'return'
t_IF = r'if'
t_DO = r'do'
t_FLOAT = 'float'
t_DOUBLE = r'double'
t_LESS = r'<'
t_GREATER = r'>'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_NUMBER(t):
  r'\d+'
  try:
    t.value = int(t.value)
  except ValueError:
    print("Line %d: Number %s is too large!" ,(t.lineno,t.value))
    t.value = 0
  return t

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
  print ("Illegal character '%s'" , t.value[0])
  t.lexer.skip(1)

def t_COMMENT(t):
    r'\#.*'
    pass

def get_lexer(data): 
	lexer = _lex.lex()
	lexer.input(data)
	return lexer
