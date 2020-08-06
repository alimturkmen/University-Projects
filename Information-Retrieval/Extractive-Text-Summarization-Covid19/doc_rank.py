from entities import Document, Term
from vectorize import Vectorizer
from functions import cos_sim, find_steady_states
from typing import Dict
import numpy as np

class Edge:
    """ Directed edge between nodes
    
    ...

    Attributes
    ----------
    id : str
        Id of the document the edge pointing
    weight : float
        Cosine similarity score between nodes
    """
    def __init__(self, id:str, weight:float):
        self.id = id
        self.weight = weight


class Node:
    """ The object for terms occur in the papers
    
    ...

    Attributes
    ----------
    id : str / int
        Id of Document or Sentence object
    body : Document / Sentence
        Document or Sentence object that node stores
    edges : List[Edge]
        List of edges that node has

    Methods
    -------
    add_ege(edge)
        Adds an edge to node
    """
    def __init__(self, body):
        self.id = body.id
        self.body = body
        self.edges = []

    def add_edge(self, edge:Edge):
        self.edges.append(edge)


class Graph:
    """ The graph of nodes and edges 
    
    ...

    Attributes
    ----------
    nodes : List[Node]
        List of nodes in the graph
    num_of_nodes : int
        Total number of nodes
    num_of_edges : List[int]
        List of number of edges of nodes
    vectorizer : Vectorizer
        Vectorizer object that return vector representation of entities

    Methods
    -------
    add_node(node)
        Adds a node to graph
    create_graph()
        Creates all edges between nodes based on cosine-similarity
    """
    def __init__(self, term_dict:Dict[str, Term]):
        self.nodes = []
        self.num_of_nodes = 0
        self.num_of_edges = []
        self.vectorizer = Vectorizer(term_dict)

    def add_node(self, node:Node):
        self.nodes.append(node)
        self.num_of_nodes += 1

    def create_graph(self):

        if type(self.nodes[0].body) == Document:
            self.vectorizer.vectorize_docs([node.body for node in self.nodes])
        else:
            self.vectorizer.vectorize_sentences([node.body for node in self.nodes])

        self.num_of_edges = [1 for i in range(self.num_of_nodes)]

        for i in range(self.num_of_nodes):
            for j in range(i+1, self.num_of_nodes):
                node1 = self.nodes[i]
                node2 = self.nodes[j]
                similarity = cos_sim(node1.body.vector, node2.body.vector)
                if similarity > 0.10:
                    node1.add_edge(Edge(node2.id, similarity))
                    node2.add_edge(Edge(node1.id, similarity))
                    self.num_of_edges[i] += 1
                    self.num_of_edges[j] += 1


class DocRank:
    """ The object that stores adjacency matrix, probability vector
    and PageRank scores
    
    ...

    Attributes
    ----------
    P : numpy.ndarray
        Transition matrix
    x : numpy.ndarray
        Probability vector of nodes
    graph : Graph
        Graph of the system
    a : numpy.ndarray
        Steady-state vector

    Methods
    -------
    start_iterations()
        Iterates system to find steady-state vector
    return_max_n(n)
        Return top-n documents(or sentences) according to PageRank
    """
    def __init__(self, graph:Graph, teleportation=0.15):

        adj_matrix=[]

        for i in range(graph.num_of_nodes):
            row = []
            node = graph.nodes[i]
            adjacents = [edge.id for edge in node.edges]
            
            for j in range(graph.num_of_nodes):
                if i==j:
                    row.append((1-teleportation) / graph.num_of_edges[i])
                    continue
                if graph.nodes[j].id in adjacents:
                    row.append((1-teleportation) / graph.num_of_edges[i] )
                else:
                    row.append(teleportation / graph.num_of_nodes)
            adj_matrix.append(row)

        self.P = np.array(adj_matrix)
        x = np.array([1/graph.num_of_nodes for i in range(graph.num_of_nodes)])
        self.x = x.T
        self.graph=graph
        self.start_iterations()

    def start_iterations(self):
        
        self.a = find_steady_states(self.x, self.P)


    def return_max_n(self, n=10):

        max_n = []
        a_index = []

        for i in range(len(self.a)):
            a_index.append((i, self.a[i]))

        def sort_by_rank(item:tuple):
            return item[1]

        sorted_indices = sorted(a_index, key=sort_by_rank, reverse=True)

        for i, (idx, score) in enumerate(sorted_indices):
            if i == n : break
            max_n.append((self.graph.nodes[idx].body, score))

        return max_n