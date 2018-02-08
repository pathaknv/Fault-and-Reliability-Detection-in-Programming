import program_graph as pg
import program_token as pt
import static_dynamic_functions as psd

data = """
	int a,b;
	int c = 10;
    b = a / c;
    if(b > 0)
    {
		c = c - 1;
    	b = b - 1;
    	a = a - 1;
    }
    else
    {
    	b = b + 3;
    	a = a + 3;
    }
    if(a > 0) 
    {
    	a = a / c;
    	b = b + 1;
    }
    a = a - b + c;
    while(c > 0)
    {
    	a = a + 5;
    	b = a + b;
    }
    a = b + c;
    a = a + b + c; 
    """

data1 = """

    int a,b;
    int c = 10;
    a = c - ;
    c = a + c;
"""
data2 = """
    int a,b,d;
    int c = 10;
    b = a / c;
    if(b > 0)
    {
        c = c - 1;
        b = b - 1;
        a = a - 1;
    }
    else
    {
        b = b + 3;
        a = a + 3;
    }
    if(a > 0 
    {
        a = a / c;
        b = b + 1;
    }
    a = a - b + c;
    whilec > 0)
    {
        a = a + 5;
        b = a + b;
    }
    a = b + c;
    a = a + b + c; 
"""
		

lexer = pt.get_lexer(data2)
data_list = pg.get_cfg(data2)
graph = data_list[0]
initial_statment = data_list[1]
pg.cyclomatic_complexity(graph)
variable_list = psd.list_of_varibales(lexer)
#print(variable_list)
#psd.divide_by_zero(graph , initial_statment , variable_list , data)
#psd.unused_varaible_detection(graph, initial_statment, variable_list)

psd.parenthesis_checker(data2)
psd.valid_expression(data1)
