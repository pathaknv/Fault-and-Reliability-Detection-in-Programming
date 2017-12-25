import re
import networkx as nx
import matplotlib.pyplot as plt
from ply import lex as _lex
from ply import yacc as _yacc

controlStmt = ['if', 'else', 'while', 'for', 'switch', 'do']
data = """
		int a,b;
		int c = 10;
        a = 0;
        b = a + 1;
        c = c + b;
        a = b * 2;
        a < 9;
        return c;
    """
tokens = ['NUMBER','PLUS','MINUS','MULT','DIVIDE','LPAREN','RPAREN','ID','COMMA','SEMICOLON','LEFTBRACE',
		'RIGHTBRACE','ASSIGN','EQUAL','LESS', 'GREATER']

reserved={
    'while' : 'WHILE',
    'else' : 'ELSE',
    'if' : 'IF',
    'for' : 'FOR',
    'switch':'SWITCH',
    'case':'CASE',
    'do' : 'DO',
    'break': 'BREAK',
    'return' : 'RETURN',
    'int' : 'INT',
    'float' : 'FLOAT',
    'double' : 'DOUBLE',
    'continue' : 'CONTINUE',
    'struct' : 'STRUCT',
    'union' : 'UNION',
    'char' : 'CHAR',
    'printf':'PRINTF',
    'scanf' : 'SCANF',
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

lexer = _lex.lex()

lexer.input(data)


def buildCFG(data):
    statment = data.split(";")
    for i in range(0, len(statment)):
        statment[i] = statment[i].strip()
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                temp = statment[i].split('\n')
                temp[1] = temp[1].strip()
                statment[i] = temp[0] + ':' + temp[1]

    del statment[-1]
    cfg = nx.DiGraph()

    initial_edge = statment[0]
    cntrlFlg = 0
    for i in range(0, len(statment)):
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                if cntrl in ['if', 'while', 'for', 'switch']:
                    temp = []
                    temp = statment[i].split(':')
                    cfg.add_node(temp[0])
                    cfg.add_node(temp[1])

                    cntrlFlg = 1;
                    break
                if cntrl == 'else':
                    cfg.add_node(statment[i])
                    cntrlFlg = 1;
                    break
        if cntrlFlg == 0:
            cfg.add_node(statment[i])
        cntrlFlg = 0

    ifFlg = 0
    elseFlg = 0
    emptyElse = 0

    for i in range(1, len(statment)):
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                if cntrl in ['if', 'while', 'for', 'switch']:
                    statment[i] = statment[i].replace('if(', '')
                    statment[i] = statment[i].replace(')', '')
                    temp = []
                    temp = statment[i].split(':')
                    ifPart = 'if(' + temp[0] + ')'
                    ifBody = temp[1]
                    cfg.add_edge(statment[i - 1], ifPart)
                    cfg.add_edge(ifPart, ifBody)
                    ifFlg = 1
                    break
                if cntrl is 'else':
                    cfg.add_edge(ifPart, statment[i])
                    elsePart = statment[i]
                    elseFlg = 1
                    break
        if ifFlg == 0 and elseFlg == 0:
            if emptyElse == 1:
                cfg.add_edge(ifPart, statment[i])
            else:
                cfg.add_edge(statment[i - 1], statment[i])
        if ifFlg == 1:
            ifFlg = 0
            if 'else' not in statment[i + 1]:
                cfg.add_edge(ifBody, statment[i + 1])
                emptyElse = 1
            else:
                cfg.add_edge(ifBody, statment[i + 2])
        if elseFlg == 1:
            cfg.add_edge(elsePart, statment[i + 1])
            elseFlg = 0
    return [cfg , initial_edge]


def cyclomaticComplexity(cfg):
    nodeCount = cfg.number_of_nodes()
    edgeCount = cfg.number_of_edges()
    cc = edgeCount - nodeCount + 2
    print('\nCyclomatic Complexity of Code: ', cc)


def cfgGUI(cfg):
    nx.draw(cfg)
    plt.savefig('cfg.png')
    plt.show()


def showEdges(cfg):
    for e in cfg.edges:
        print(e)


def showNodes(cfg):
    for n in cfg.nodes:
        print(n)

def simple_traversal(initial_edge):
	edgeList = []
	edgeList.append(initial_edge)
	i = 0
	while i < len(edgeList):
		temp_edge_list = list(cfg.edges(edgeList[i]))
		print(edgeList[i])
		for temp_edge in temp_edge_list:
			edgeList.append(temp_edge[1])
		i+=1
	return edgeList

def list_of_varibales():
	variable_list = {}
	flg = 0
	while 1:
		tok = lexer.token()
		if not tok: break  
		if tok.type in ['INT' , 'FLOAT' , 'DOUBLE' , 'CHAR']:
			tok = lexer.token()
			variable_list[tok.value] = 0
			last_variable = tok.value
			while tok.type != 'SEMICOLON': 
				tok = lexer.token()
				if tok.type == 'COMMA':
					tok = lexer.token()
					variable_list[tok.value] = 0
					last_variable = tok.value
				elif tok.type == 'ASSIGN':
					tok = lexer.token()
					variable_list[last_variable] = tok.value;
	return variable_list

cfg = nx.DiGraph
data_list = buildCFG(data)
cfg = data_list[0]
initial_edge = data_list[1]
cyclomaticComplexity(cfg)

#cfgGUI(cfg)
#edgeList = list(nx.bfs_edges(cfg, 'y = x / 2'))
print('\n')
edgeList = simple_traversal(initial_edge)
print('\n')
variable_list = list_of_varibales()
print(variable_list)
