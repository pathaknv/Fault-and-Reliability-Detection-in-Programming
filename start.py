import program_graph as pg
import program_token as pt
import static_dynamic_functions as psd

data = """
	int a,b;
	int c = 0;
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
    	a = a / 0;
    	b = b + 1;
    }
    a = a - b + c;
    while(c > 0)
    {
    	a = a + 5;
    	b = a + b;
    }
    a = b + c;
    for(i=0; i<100; i++)
    {
    	a = a + i;
    	b = c + i; 
    }
    a = a + b + c; 
    """
		

lexer = pt.get_lexer(data)
data_list = pg.get_cfg(data)
graph = data_list[0]
initial_statment = data_list[1]
pg.cyclomatic_complexity(graph)
variable_list = psd.list_of_varibales(lexer)
print(variable_list)
psd.divide_by_zero(graph , initial_statment , variable_list , data) 
