import networkx as nx
import graphviz as gv
g1 = gv.Digraph(format='png')
g1.attr('graph', bgcolor='#FFFFFF',label='Control Flow Graph',fontcolor='white',fontsize='16')
g1.attr('node',fontname='Helvetica',fontcolor='black',color='black',style='filled',fillcolor='#FFFFFF')
g1.attr('edge',style ='dashed',color='black',arrowhead='open',fontname='Courier',fontsize='12',fontcolor='black')
controlStmt = ['if', 'else', 'while', 'for', 'switch', 'do']

def data_pre_processing(data):
    statment = data.split("\n")
    for i in range(0, len(statment)):
        if 'for' not in statment[i]:
            statment[i] = statment[i].strip()
            statment[i] = statment[i].replace(';' , '')

    del statment[0]
    del statment[-1]
    return statment

def buildCFG(data):

    cntrl_flg = 0
    if_flg = 0
    while_flg = 0
    for_flg = 0
    else_flg = 0
    statment = data_pre_processing(data)
    cfg = nx.DiGraph()
    initial_statment = statment[0]

    for i in range(0 , len(statment)):
        if statment[i] not in ['{' , '}' , 'else']:
            cfg.add_node(statment[i])
            g1.node(statment[i])

    for i in range(0 , len(statment) - 1):

        if cntrl_flg != 1:
            for cntrl in controlStmt:
                if cntrl in statment[i]:
                    cntrl_flg = 1
                    control_statment = statment[i]
                    if cntrl == 'if':
                        if_flg = 1
                    if cntrl == 'while':
                        while_flg = 1
                    if cntrl == 'for':
                        for_flg = 1

        if cntrl_flg == 0:
            cfg.add_edge(statment[i] , statment[i+1])
            g1.edge(statment[i], statment[i+1])

        if while_flg == 1 or for_flg == 1:

            if 'while' in  statment[i] or 'for' in statment[i]:
                cfg.add_edge(statment[i] , statment[i+2])
                g1.edge(statment[i], statment[i+2])
            elif statment[i] != '{' and statment[i+1] != '}' and statment[i] != '}':
                cfg.add_edge(statment[i] , statment[i+1])
                g1.edge(statment[i], statment[i+1])


            if statment[i] == '}':
                if i+1 <= len(statment):
                    cfg.add_edge(control_statment , statment[i+1])
                    g1.edge(control_statment , statment[i+1])
                    cfg.add_edge(statment[i-1] , control_statment)
                    g1.edge(statment[i-1] , control_statment)
                else:
                    cfg.add_edge(statment[i-1] , control_statment)
                    g1.edge(statment[i-1] , control_statment)

                cntrl_flg = 0
                if while_flg == 1:
                    while_flg = 0
                else:
                    for_flg = 0

        if else_flg == 1:

            if statment[i] == 'else':
                cfg.add_edge(control_statment , statment[i+2])
                g1.edge(control_statment , statment[i+2])
            elif statment[i] !='{' and statment[i+1] != '}' and statment[i] != '}':
                cfg.add_edge(statment[i] , statment[i+1])
                g1.edge(statment[i] , statment[i+1])


            if statment[i] == '}':
                cntrl_flg = 0
                else_flg = 0
                if i+1 <= len(statment):
                     cfg.add_edge(last_if_statment , statment[i+1])
                     g1.edge(last_if_statment  , statment[i+1])
                     cfg.add_edge(statment[i-1] , statment[i+1])
                     g1.edge(statment[i-1]  , statment[i+1])

        if if_flg == 1:

            if 'if' in statment[i]:
                cfg.add_edge(statment[i] , statment[i+2])
                g1.edge(statment[i]  , statment[i+2])
            elif statment[i] !='{' and statment[i+1] != '}' and statment[i] != '}':
                cfg.add_edge(statment[i] , statment[i+1])
                g1.edge(statment[i]  , statment[i+1])

            if statment[i] == '}':
                if i+1 <= len(statment):
                    if statment[i+1] == 'else':
                        last_if_statment = statment[i-1]
                        else_flg = 1
                        if_flg = 0
                    else:
                        if_flg = 0
                        cntrl_flg = 0
                        cfg.add_edge(statment[i-1] , statment[i+1])
                        g1.edge(statment[i-1]  , statment[i+1])
                        cfg.add_edge(control_statment , statment[i+1])
                        g1.edge(control_statment , statment[i+1])

    #print(g1.source)
    filename = g1.render(filename='img/g1')
    return [cfg , initial_statment, g1]

def cyclomatic_complexity(cfg):
    nodeCount = cfg.number_of_nodes()
    edgeCount = cfg.number_of_edges()
    cc = edgeCount - nodeCount + 2
    print('\nCyclomatic Complexity of Code: ', cc)

def get_cfg(data):
    cfg = nx.DiGraph
    data_list = buildCFG(data)
    return data_list

def show_nodes(cfg):
    print(cfg.nodes())

def show_edges(cfg):
    for edge in cfg.edges():
        print(edge)

def cfgGUI(cfg):
    nx.draw(cfg)
    plt.savefig('cfg.png')
    plt.show()
