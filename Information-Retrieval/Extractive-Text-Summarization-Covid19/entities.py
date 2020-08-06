from typing import List
from math import log

class Topic:
    """ The object for topics in the system 
    
    ...

    Attributes
    ----------
    id : int
        The id of the topic
    query : str
        Content of the topic
    question : str
        Question that the topic seeks answers
    narrative : Tensor
        Detailed explanation of the content
    """
    def __init__(self, id, query=None, question=None, narrative=None):
        self.id = id
        self.query = query
        self.question = question
        self.narrative = narrative


class Document:
    """ The object for papers in the system
    
    ...

    Attributes
    ----------
    topic : int
        The id of the paper's topic
    id : str
        Document id (cord-id)
    relevance : int
        Relevance-judgement ranging 0 to 2
    abstract : str
        Abstract of the paper
    sent_list : List[str]
        List of sentences in the abstract
    vector : numpy.ndarray
        TF-IDF vector representation of the document

    Methods
    -------
    set_abstract(abstract)
        Sets the abstract
    set_sent_list(sent_list)
        Sets the sentence list 
    set_vector(vector)
        Assigns the numpy vector 
    """
    def __init__(self, topic, id, relevance):
        self.topic = topic
        self.id = id
        self.relevance = int(relevance)
        self.abstract = ''
        self.sent_list = []

    def set_abstract(self, abstract:str):
        self.abstract = abstract

    def set_sent_list(self, sent_list:List[str]):
        self.sent_list = sent_list

    def set_vector(self, vector):
        self.vector = vector

class Term:
    """ The object for terms occur in the papers
    
    ...

    Attributes
    ----------
    name : str
        The term itself
    df : int
        Document frequency of the term
    idf : int
        Inverse-document frequency of the term

    Methods
    -------
    calculate_idf(num_of_docs)
        Calculates idf score of the term
    """
    def __init__(self, name):
        self.name = name
        self.df = 1

    def calculate_idf(self, num_of_docs:int):
        self.idf = log(num_of_docs/self.df) + 1


class Sentence:
    """ The object for sentences in the abstracts
    
    ...

    Attributes
    ----------
    id : int
        Sentence id
    doc_id : str
        Document id that sentence belongs to
    text : str
        The sentence itself

    Methods
    -------
    set_vector(vector)
        Assigns numpy vector representation of the sentence
    """
    def __init__(self, id:int, doc_id:str, text:str):
        self.id = id
        self.doc_id = doc_id
        self.text = text

    def set_vector(self, vector):
        self.vector = vector