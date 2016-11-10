class State(object):
    def __init__(self,word):
        self.word = word
        self.substates = []
    def add_substate(self, tag):
        sub = Substate(tag)
        self.substates.append(sub)

class Edge(object):
    def __init__(self,end,weight):
        self.start_node = end
        self.weight = weight

class Substate(object):
    def __init__(self,tag):
        self.tag = tag
        self.edges = [] 
        self.viterbi = 0.
        self.back_point = None
    def add_edge(self,end_node,weight):
        edge = Edge(end_node, weight)
        self.edges.append(edge)

