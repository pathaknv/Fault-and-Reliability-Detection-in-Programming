import networkx as nx
import matplotlib.pyplot as plt

controlStmt = ['if' , 'else' , 'while' ,'for' , 'switch' , 'do']
data = """
            y = x / 2;
            if(y > 3)
                x = x - y;
            else
                x = x + y;
            z = x - 4;
            if(z > 0)
                x = x / 2;
            else 
                x = x * 2;
            z = z - 1;
        """
def buildCFG(data):
    statment = data.split(";")
    for i in range(0 , len(statment)):
        statment[i] = statment[i].strip()
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                temp = statment[i].split('\n')
                temp[1] = temp[1].strip()
                statment[i] = temp[0] + ':' + temp[1]

    del statment[-1]
    cfg = nx.DiGraph()

    cntrlFlg = 0
    for i in range(0 , len(statment)):
        for cntrl in controlStmt:
            if cntrl in statment[i]:
                if cntrl in ['if' , 'while' , 'for' , 'switch']:
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

    for i in range(1 , len(statment)):
        for cntrl in controlStmt: 
            if cntrl in statment[i]:
                if cntrl in ['if' , 'while' , 'for' , 'switch']:
                    statment[i] = statment[i].replace('if(' , '')
                    statment[i] = statment[i].replace(')' , '')
                    temp = []
                    temp = statment[i].split(':')
                    ifPart = 'if(' + temp[0] + ')'
                    ifBody = temp[1]
                    cfg.add_edge(statment[i-1] , ifPart)
                    cfg.add_edge(ifPart , ifBody)
                    ifFlg = 1
                    break
                if cntrl is 'else':
                    cfg.add_edge(ifPart , statment[i])
                    elsePart = statment[i]
                    elseFlg = 1
                    break
        if ifFlg == 0 and elseFlg == 0:
            if emptyElse == 1:
                cfg.add_edge(ifPart , statment[i])
            else:
                cfg.add_edge(statment[i-1] , statment[i])
        if ifFlg == 1:  
            ifFlg = 0
            if 'else' not in statment[i+1]:
                cfg.add_edge(ifBody , statment[i+1])
                emptyElse = 1
            else:
                cfg.add_edge(ifBody , statment[i+2])
        if elseFlg == 1:
            cfg.add_edge(elsePart , statment[i+1])
            elseFlg = 0
    return cfg

def cyclomaticComplexity(cfg):
    
    nodeCount = cfg.number_of_nodes()
    edgeCount = cfg.number_of_edges()
    cc = edgeCount - nodeCount + 2
    print('\nCyclomatic Complexity of Code: ',cc)
    
def cfgGUI(cfg):
    nx.draw(cfg)
    plt.savefig('cfg.png')
    plt.show()
    
def showEdges(cfg):
    for e in cfg.edges:
        print(e)

def showNodes(cfg):
    for n in cfg.nodes:
        print(n)
    

cfg = nx.DiGraph
cfg = buildCFG(data)
showEdges(cfg)
print('\n')
showNodes(cfg)
cyclomaticComplexity(cfg)

cfgGUI(cfg)

    