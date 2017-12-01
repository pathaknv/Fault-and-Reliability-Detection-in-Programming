import program_graph as pg
import program_token as pt

data = """
	int a,b,c;
	int c = 10;
        b = a / c;
        c = c + b;
        a = b + 2;
    """

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

def divide_by_zero(graph , initial_edge , variable_list):

	flg = 0
	while 1:
		if len(initial_edge) == 0:
			break
		lexer = pt.get_lexer(initial_edge)
		while 1:
			tok = lexer.token()
			if not tok:
				temp_edge = list(graph.edges(initial_edge))
				if len(temp_edge) == 0:
					flg = 1
					break
				initial_edge = temp_edge[0][1]
				break
			if tok.type == 'ASSIGN':
				tok = lexer.token()
				tok = lexer.token()
				if not tok:
					temp_edge = list(graph.edges(initial_edge))
					if len(temp_edge) == 0:
						flg = 1
						break
					initial_edge = temp_edge[0][1]
					break
				if tok.type == 'DIVIDE':
					tok = lexer.token()
					if variable_list[tok.value] == 0:
						print('Divide by Zero Error')
		if flg == 1:
			break				

lexer = pt.get_lexer(data)
data_list = pg.get_cfg(data)

graph = data_list[0]
initial_edge = data_list[1]
pg.cyclomatic_complexity(graph)

variable_list = list_of_varibales()
divide_by_zero(graph , initial_edge , variable_list)
