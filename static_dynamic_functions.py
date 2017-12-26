import program_graph as pg
import program_token as pt

def list_of_varibales(lexer):
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

def get_error_line_number(current_edge , data):

	statment_list = pg.data_pre_processing(data)
	for i in range(0 , len(statment_list)):
		if statment_list[i] == current_edge:
			print('Divide By Zero on Line Number: ',i+1)
			break

def divide_by_zero(graph , initial_statment , variable_list , data):

	divide_flg = 0
	divide_by_zero_list = []
	statment_stack = []
	statment_stack.append(initial_statment)

	while 1:
		if len(statment_stack) == 0:
			break
		current_edge = statment_stack[0]
		del statment_stack[0]
		next_edge = list(graph.edges(current_edge))
		if len(next_edge) == 0:
			break

		i = 0
		while i < len(next_edge):
			statment_stack.append(next_edge[i][1])
			i += 1
		
		lexer = pt.get_lexer(current_edge)
		while 1:
			tok = lexer.token()
			if not tok:
				break
			if tok.type == 'DIVIDE':
				tok = lexer.token()
				if tok.type == 'ID' and variable_list[tok.value] == 0 or tok.type == 'NUMBER' and tok.value == 0:
					flg = 0
					for i in range(0 , len(divide_by_zero_list)):
						if divide_by_zero_list[i] == current_edge:
							flg = 1
							break
					if flg != 1:
						get_error_line_number(current_edge , data)
						divide_by_zero_list.append(current_edge)
