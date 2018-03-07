import program_graph as pg
import program_token as pt
import static_dynamic_functions as psd

data = """
int x,y = 5;
int z = 10;
x = z - 5;
if(x > 5)
{
  x = x - 1;
}
else
{
x = x + 1;
}
z = x + z;
    """


lexer = pt.get_lexer(data)
data_list = pg.get_cfg(data)
graph = data_list[0]
initial_statment = data_list[1]

variable_list = psd.list_of_varibales(lexer)

while 1:
    print('\nMenu\n1. CFG Nodes and Edges\n2. CFG GUI\n3. Cyclomatic Complexity\n4. Divide By Zero')
    print('5. Unused Variable Detection\n6. Parenthesis Checker\n7. Memory Statistics')
    print('8. Exit')
    option = input()

    if option == '1':
        print('\n CFG Nodes')
        pg.show_nodes(graph)
        print('\n CFG Edges')
        pg.show_edges(graph)

    if option == '2':
        print(data_list[2].render(filename='img/g1', view=True))

    if option == '3':
        pg.cyclomatic_complexity(graph)

    if option == '4':
        psd.divide_by_zero(graph , initial_statment , variable_list , data)

    if option == '5':
        psd.unused_variable_detection(graph, initial_statment, variable_list)

    if option == '6':
        psd.parenthesis_checker(data)

    if option == '7':
        lexer = pt.get_lexer(data)
        variable_count = psd.category_wise_variable_count(lexer)
        lexer = pt.get_lexer(data)
        memory_statistics = psd.memory_usage(graph, initial_statment, variable_list, variable_count, lexer)
        print('Total Memory used by variables: ', memory_statistics[0])
        print('Total Memory used after optimization: ',memory_statistics[0] - memory_statistics[1])

    if option == '9':
        psd.valid_expression(data)

    if option == '8':
        break
