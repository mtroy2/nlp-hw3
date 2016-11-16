class State(object):
    def __init__(self,word):
        self.word = word
        self.substates = []
    def add_substate(self, tag,weight):
        sub = Substate(tag,weight)
        self.substates.append(sub)

class Edge(object):
    def __init__(self,end,weight):
        self.start_node = end
        self.weight = weight

class Substate(object):
    def __init__(self,tag,weight):
        self.tag = tag
        self.edges = [] 
        self.viterbi = -100
        self.word_weight = weight
        self.back_point = None
    def add_edge(self,end_node,weight):
        edge = Edge(end_node, weight)
        self.edges.append(edge)

