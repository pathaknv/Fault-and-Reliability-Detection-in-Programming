import program_graph as pg
import program_token as pt

comparision_operators = ['>' , '<' , '>=' , '<=' , '==']
binary_operators = ['+', '-', '*', '/', '==', '>=', '<=', '>', '<']

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


def data_flow(graph, initial_statment, variable_list):
		
	varaible_access_status = []
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
						varaible_access_status.append(lhs_variable)

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
							if current_token.type != 'NUMBER' and current_token.value not in varaible_access_status:
								varaible_access_status.append(current_token.value)
		
						else:
							if current_token.type == 'NUMBER':
								rhs_value = current_token.value
							else:
								rhs_value = variable_list[current_token.value]
								varaible_access_status.append(current_token.value)

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

	return varaible_access_status

def unused_varaible_detection(graph, initial_statment, variable_list):
	varaible_access_status = data_flow(graph, initial_statment, variable_list)
	for variable in variable_list.keys():
		if variable not in varaible_access_status:
			print('Variable "',variable, '" is not used in program')

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
	for i in range(0 , len(statment_list)):
		if balanced_parenthesis(statment_list[i]) == False:
			print('Unbalanced Parenthesis on Line Number: ',i+1)

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
					
