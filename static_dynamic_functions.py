import program_graph as pg
import program_token as pt

comparision_operators = ['>' , '<' , '>=' , '<=' , '==']

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


def calculate_all_loop_iterations(graph , initial_statment , variable_list):
		
	statment_stack = []
	statment_stack.append(initial_statment)
	if_flg = 0
	ans_flg = 0
	while 1:

		if len(statment_stack) == 0:
			break
		current_edge = statment_stack[0]
		del statment_stack[0]

		lexer = pt.get_lexer(current_edge)
		current_token = lexer.token()
		previous_token = current_token

		if 'if' in current_edge:
			temp_edge = current_edge
			temp_edge = temp_edge.replace('if(' , '')
			temp_edge = temp_edge.replace(')' , '')
			lexer = pt.get_lexer(temp_edge)
			current_token = lexer.token()
			lhs_variable
			ans_flg = 0
			if_flg = 1
			operator_flg = 0
			operator_type = 'NOTHING'
			while 1:
				if not current_token:
					break
				if operator_flg != 0:

					if operator_type == '>':
						if current_token.type == 'NUMBER':
							if variable_list[lhs_variable] > current_token.value:
								ans_flg = 1
						else:
							if variable_list[lhs_variable] > variable_list[current_token.value]:
								ans_flg = 1 

				else:
					if current_token.value in comparision_operators:
						operator_flg = 1
						operator_type = current_token.value
					else:
						lhs_variable = current_token.value

				current_token = lexer.token()
		else:
			assign_flg = 0
			rhs_value = 0
			operator_flg = 0
			operator_type = "NOTHING"
			while 1:
				if not current_token:
					break

				if assign_flg == 1:
					if current_token.type != 'ID' and current_token.type != 'NUMBER':
						operator_flg = 1
						operator_type = current_token.type
					else:
						if operator_flg == 1:

							if operator_type == 'DIVIDE':
								if current_token.type == 'NUMBER': 
									rhs_value = rhs_value / current_token.value
								else:
									rhs_value = rhs_value / variable_list[current_token.value]
								variable_list[lhs_variable] = rhs_value

							if operator_type == 'MULT':
								if current_token.type == 'NUMBER': 
									rhs_value = rhs_value * current_token.value
								else:
									rhs_value = rhs_value * variable_list[current_token.value]
								variable_list[lhs_variable] = rhs_value
									
							if operator_type == 'PLUS':
								if current_token.type == 'NUMBER': 
									rhs_value = rhs_value + current_token.value
								else:
									rhs_value = rhs_value + variable_list[current_token.value]
								variable_list[lhs_variable] = rhs_value

							if operator_type == 'MINUS':
								if current_token.type == 'NUMBER': 
									rhs_value = rhs_value - current_token.value
								else:
									rhs_value = rhs_value - variable_list[current_token.value]
								variable_list[lhs_variable] = rhs_value	
		
						else:
							if current_token.type == 'NUMBER':
								rhs_value = current_token.value
							else:
								rhs_value = variable_list[current_token.value]

				if current_token.type == 'ASSIGN':
					lhs_variable = previous_token.value
					assign_flg = 1

				previous_token = current_token
				current_token = lexer.token()


		next_edge = list(graph.edges(current_edge))
		if len(next_edge) == 0:
			break

		i = 0
		while i < len(next_edge):
			statment_stack.append(next_edge[i][1])
			i += 1

		if if_flg == 1:
			if ans_flg == 1:
				del statment_stack[1]
			else:
				del statment_stack[0]
			if_flg = 0

		print(variable_list)
		print(statment_stack)
