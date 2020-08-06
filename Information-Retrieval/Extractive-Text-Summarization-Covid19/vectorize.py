from entities import Document, Term, Sentence
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from typing import List, Dict


class Vectorizer():
    """ The object for extract representative tf-idf vectors of 
    sentences and documents 
    
    ...

    Attributes
    ----------
    tokenizer : RegexpTokenizer
        Tokenizes text pieces
    term_dict : Dict[str, Term]
        Term dictionary to create vectors

    Methods
    -------
    vectorize_doc(doc)
        Sets the vector of the given Document doc
    vectorize_docs(doc_list)
        Sets the vectors of the given documents in doc_list
    vectorize_sentence(sent)
        Sets the vector of the given Sentence sent
    vectorize_sentences(sent_list)
        Sets the vectors of the given sentences in sent_list
    """
    def __init__(self, term_dict:Dict[str, Term]):
        self.tokenizer = RegexpTokenizer(r'[a-z|A-Z]+')
        self.term_dict = term_dict


    def vectorize_doc(self, doc:Document) -> np.ndarray:
        vector = np.array([])
        
        abstract_tokens = self.tokenizer.tokenize(doc.abstract.lower())

        term_frequency = {}

        for term in abstract_tokens:
            if term in term_frequency:
                term_frequency[term] += 1
            else:
                term_frequency[term] = 1

        for term in self.term_dict:
            if term in term_frequency:
                tf = term_frequency[term]
                vector = np.append(vector, [self.term_dict[term].idf * tf])
            else:
                vector = np.append(vector, [0])

        doc.set_vector(vector)
        return vector


    def vectorize_docs(self, doc_list:Dict[str, Document]):

        vectors = {}

        for doc in doc_list:
            vectors[doc] = self.vectorize_doc(doc)

        return vectors


    def vectorize_sentence(self, sent:Sentence) -> np.ndarray:
        vector = np.array([])
        
        sent_tokens = self.tokenizer.tokenize(sent.text.lower())

        term_frequency = {}

        for term in sent_tokens:
            if term in term_frequency:
                term_frequency[term] += 1
            else:
                term_frequency[term] = 1

        for term in self.term_dict:
            if term in term_frequency:
                tf = term_frequency[term]
                vector = np.append(vector, [self.term_dict[term].idf * tf])
            else:
                vector = np.append(vector, [0])

        sent.set_vector(vector)
        return vector


    def vectorize_sentences(self, sent_list:List[Sentence]):

        sent_vectors = []

        for sent in sent_list:
            sent_vectors.append(self.vectorize_sentence(sent))

        return sent_vectors

        