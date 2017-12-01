import networkx as nx
import matplotlib.pyplot as plt

controlStmt = ['if', 'else', 'while', 'for', 'switch', 'do']

def buildCFG(data):
    statment = data.split(";")
    for i in range(0, len(statment)):
        statment[i] = statment[i].strip()
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                temp = statment[i].split('\n')
                temp[1] = temp[1].strip()
                statment[i] = temp[0] + ':' + temp[1]

    del statment[-1]
    cfg = nx.DiGraph()

    initial_edge = statment[0]
    cntrlFlg = 0
    for i in range(0, len(statment)):
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                if cntrl in ['if', 'while', 'for', 'switch']:
                    temp = []
                    temp = statment[i].split(':')
                    cfg.add_node(temp[0])
                    cfg.add_node(temp[1])

                    cntrlFlg = 1;
                    break
                if cntrl == 'else':
                    cfg.add_node(statment[i])
                    cntrlFlg = 1;
                    break
        if cntrlFlg == 0:
            cfg.add_node(statment[i])
        cntrlFlg = 0

    ifFlg = 0
    elseFlg = 0
    emptyElse = 0

    for i in range(1, len(statment)):
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                if cntrl in ['if', 'while', 'for', 'switch']:
                    statment[i] = statment[i].replace('if(', '')
                    statment[i] = statment[i].replace(')', '')
                    temp = []
                    temp = statment[i].split(':')
                    ifPart = 'if(' + temp[0] + ')'
                    ifBody = temp[1]
                    cfg.add_edge(statment[i - 1], ifPart)
                    cfg.add_edge(ifPart, ifBody)
                    ifFlg = 1
                    break
                if cntrl is 'else':
                    cfg.add_edge(ifPart, statment[i])
                    elsePart = statment[i]
                    elseFlg = 1
                    break
        if ifFlg == 0 and elseFlg == 0:
            if emptyElse == 1:
                cfg.add_edge(ifPart, statment[i])
            else:
                cfg.add_edge(statment[i - 1], statment[i])
        if ifFlg == 1:
            ifFlg = 0
            if 'else' not in statment[i + 1]:
                cfg.add_edge(ifBody, statment[i + 1])
                emptyElse = 1
            else:
                cfg.add_edge(ifBody, statment[i + 2])
        if elseFlg == 1:
            cfg.add_edge(elsePart, statment[i + 1])
            elseFlg = 0
    return [cfg , initial_edge]

def cyclomatic_complexity(cfg):
    nodeCount = cfg.number_of_nodes()
    edgeCount = cfg.number_of_edges()
    cc = edgeCount - nodeCount + 2
    print('\nCyclomatic Complexity of Code: ', cc)

def get_cfg(data):
	cfg = nx.DiGraph
	data_list = buildCFG(data)
	return data_list
