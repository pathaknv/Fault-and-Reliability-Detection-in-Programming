import program_graph as pg
import program_token as pt

comparision_operators = ['>' , '<' , '>=' , '<=' , '==']
binary_operators = ['+', '-', '*', '/', '==', '>=', '<=', '>', '<']
variable_memory_mapping = { 'int': 4, 'float': 4, 'double': 8, 'char': 1}

def memory_usage(graph, initial_statment, variable_list, variable_count, lexer):
	total_memory = 0
	for key,value in variable_count.items():
		total_memory = total_memory + variable_memory_mapping[key]*value
	variable_access_status = data_flow(graph, initial_statment, variable_list)


	while 1:
		tok = lexer.token()
		if not tok: break
		if tok.type in ['INT' , 'FLOAT' , 'DOUBLE' , 'CHAR']:
			variable_type = str(tok.type).lower()
			tok = lexer.token()
			if str(tok.value) in variable_access_status:
				variable_count[variable_type] -= 1
				tok = lexer.token()
				while tok.type != 'SEMICOLON':
					tok = lexer.token()
					if tok.type == 'COMMA':
						tok = lexer.token()
						if tok.value in variable_access_status:
							variable_count[variable_type] -= 1

	memory_with_unused_variable = 0
	for key,value in variable_count.items():
		memory_with_unused_variable += variable_memory_mapping[key]*value
	return [total_memory, memory_with_unused_variable]

def category_wise_variable_count(lexer):
	variable_count = {}
	variable_count['int'] = 0
	variable_count['float'] = 0
	variable_count['double'] = 0
	variable_count['char'] = 0
	while 1:
		tok = lexer.token()
		if not tok:
			break
		if tok.type in ['INT', 'FLOAT', 'DOUBLE', 'CHAR']:
			variable_count[str(tok.type).lower()] = variable_count[str(tok.type).lower()] + 1
			variable_type = tok.type
			tok = lexer.token()
			while tok.type != 'SEMICOLON':
				tok = lexer.token()
				if tok.type == 'COMMA':
					variable_count[str(variable_type).lower()] = variable_count[str(variable_type).lower()] + 1
	return variable_count

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
	error_flg = 0

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
						error_flg = 1
						get_error_line_number(current_edge , data)
						divide_by_zero_list.append(current_edge)

	if error_flg == 0:
		print('\nNone Divide by zero')

def data_flow(graph, initial_statment, variable_list):

	variable_access_status = []
	statment_stack = []
	statment_stack.append(initial_statment)
	used_variable_type = {}
	used_variable_type['int'] = 0
	used_variable_type['float'] = 0
	used_variable_type['double'] = 0
	used_variable_type['char'] = 0
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
						variable_access_status.append(lhs_variable)

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
							if current_token.type != 'NUMBER' and current_token.value not in variable_access_status:
								variable_access_status.append(current_token.value)

						else:
							if current_token.type == 'NUMBER':
								rhs_value = current_token.value
							else:
								rhs_value = variable_list[current_token.value]
								if current_token.value not in variable_access_status:
									variable_access_status.append(current_token.value)

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

	return variable_access_status

def unused_variable_detection(graph, initial_statment, variable_list):
	variable_access_status = data_flow(graph, initial_statment, variable_list)
	error_flg = 0
	for variable in variable_list.keys():
		if variable not in variable_access_status:
			error_flg = 1
			print('Variable "',variable, '" is not used in program')

	if error_flg == 0:
		print('\nNo unused variable detected')

def balanced_parenthesis(symbolString):
    s = []
    balanced = True
    index = 0
    while index < len(symbolString) and balanced:
        symbol = symbolString[index]
        if symbol == "(":
            s.append(symbol)
        else:
            if len(s) == 0 and symbol in ['(', ')']:
                balanced = False
            elif symbol == ')':
                s.pop()

        index = index + 1

    if balanced and len(s) == 0:
        return True
    else:
        return False

def parenthesis_checker(data):
	statment_list = pg.data_pre_processing(data)
	error_flg = 0
	print('')
	for i in range(0 , len(statment_list)):
		if balanced_parenthesis(statment_list[i]) == False:
			error_flg = 1
			print('Unbalanced Parenthesis on Line Number: ',i+1)

	if error_flg == 0:
		print('\nBalanced Parenthesis')

def valid_expression(data):
	statment_list = pg.data_pre_processing(data)
	for i in range(0, len(statment_list)):
		lexer = pt.get_lexer(statment_list[i])
		current_token = ''
		previous_token = ''
		while 1:
			if not current_token:
				break
			current_token = lexer.token()
			if current_token.value in binary_operators:
				if previous_token.type == 'ID':
					current_token = lexer.token()
					if current_token.type != 'ID':
						print('Invalid Equation at Line Number: ', i+1)
