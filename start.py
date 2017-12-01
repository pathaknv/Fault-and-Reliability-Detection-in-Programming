import program_graph as pg
import program_token as pt

data = """
		int a,b;
		int c = 10;
        a = 0;
        b = a + 1;
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
		assign_flg = 0
		if len(initial_edge) ==0 :
			break
		lexer = pt.get_lexer(initial_edge)
		while 1:
			tok = lexer.token()
			if not tok:
				temp_edge = list(graph.edges(initial_edge))
				if len(temp_edge) == 0:
					flg = 1
					break;
				initial_edge = temp_edge[0][1] 
				break
			print("Token")
			if tok.type == 'ID' and assign_flg == 0:
				left_varibale = tok.value
			elif tok.type == 'ASSIGN':
				assign_flg = 1
				value = 0
				while 1:
					tok = lexer.token()
					if not tok: 
						break
					if tok.type == 'ID':
						value = variable_list[tok.value]
					if tok.type == 'PLUS':
						tok = lexer.token()
						if tok.type == 'ID':
							value = value + variable_list[tok.value]
							print(value,' = ',value,' + ',variable_list[tok.value])
						else:
							value = value + tok.value
				variable_list[left_varibale] = value		

		if flg == 1:
			break


lexer = pt.get_lexer(data)
data_list = pg.get_cfg(data)

graph = data_list[0]
initial_edge = data_list[1]
pg.cyclomatic_complexity(graph)

variable_list = list_of_varibales()
print(variable_list)
divide_by_zero(graph , initial_edge , variable_list)
print(variable_list)