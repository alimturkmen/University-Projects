"""Dedicated Document Parser

The functions in this simple module are to be used for reading 
procesing summarization-system-related files. Three different
types of files are parsed: xml, txt and csv. `xml` module is used
for processing xml file whereas csv is used for reading csv.

This file contains the following functions:

    * read_topic_doc() - Reads topics.xml file and returns a dictionary
    where keys are topic-ids and values are Topic objects

    * read_relevance_doc() - Reads relevance.txt file and returns a
    dictionary of Document objects that have relevance score 2

    * read_docs() - Parses metadata.csv file, extracts abstracts for
    documents in given Document dictionary and captures terms in 
    abstracts to create term-dictionary that is to be returned
"""


from xml.etree.ElementTree import ElementTree
from entities import Document, Topic, Term
from typing import Dict, List
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import csv

def read_topic_doc(path='./data/topics.xml') -> Dict[str, Topic]:
    
    topic_dict = {}

    topics = ElementTree().parse(source=path)

    for idx, topic in enumerate(topics):
        
        fields = {'id':idx+1, 'query':None, 'question':None, 'narrative':None}

        for item in topic:
            fields[item.tag] = item.text
        t = Topic(fields['id'], fields['query'], fields['question'], fields['narrative'])
        topic_dict[idx+1] = t

    return topic_dict


def read_relevance_doc(path='./data/relevance.txt') -> Dict[str, Dict[str, Document]]: 

    relevance_dict = {}

    with open(path, 'r') as f:
        for line in f.readlines():
            tokens = line.split(' ')
            topic_id, doc_id, relevance = int(tokens[0]), tokens[3], tokens[4].replace('\n', '')
            if relevance != '2': continue
            d = Document(topic_id, doc_id, relevance)
            if topic_id in relevance_dict:
                relevance_dict[topic_id][doc_id] = d
            else:
                relevance_dict[topic_id] = {}
                relevance_dict[topic_id][doc_id] = d
            
    return relevance_dict


def read_docs(path='./data/metadata.csv', doc_list:Dict[str, Document]=None) -> Dict[str, Term]:

    global stopwords

    doc_abstracts = {}
    term_dict = {}
    _stopwords = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'[a-z|A-Z]+')
    num_of_docs = 0

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='\"')
        
        for row in reader:
            if len(row) < 9:
                doc_abstracts[row[0]] = ''
                continue
            doc_id, abstract = row[0], row[8]

            doc_abstracts[doc_id] = abstract
            words = tokenizer.tokenize(abstract.lower())


            for word in set(words):
                if word in _stopwords: continue
                if word in term_dict:
                    term_dict[word].df += 1
                else:
                    term_dict[word] = Term(word)

            if not abstract == '' : num_of_docs += 1
    
    rare_terms = []

    for term in term_dict:
        if term_dict[term].df == 1:
            rare_terms.append(term)
            continue
        term_dict[term].calculate_idf(num_of_docs)

    for term in rare_terms:
        term_dict.pop(term)

    for doc in doc_list:
        abstract = doc_abstracts[doc]
        doc_list[doc].set_abstract(abstract)
        sent_list = sent_tokenize(abstract, 'english')
        doc_list[doc].set_sent_list(sent_list)
    
    
    return term_dict