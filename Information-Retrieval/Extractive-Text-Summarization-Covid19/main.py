from entities import Document, Topic, Sentence
import parse
from doc_rank import Graph, Node, DocRank
import sys

def get_summary_sentences(topic_id:int):
    
    global all_docs, topic_details
    
    
    topic_docs = all_docs[topic_id]

    """ Dictionary of Term objects """
    term_dict = parse.read_docs(doc_list=topic_docs)

    """ Document graph that will contain edges between documents """
    doc_graph = Graph(term_dict)

    for doc in topic_docs:
        doc_graph.add_node(Node(topic_docs[doc])) 

    doc_graph.create_graph() #The edges are created

    """ The adjaceny matrix for docs which conducts PageRank  """
    doc_rank = DocRank(doc_graph) 

    """ List of most rated 10 documents """
    doc_list = doc_rank.return_max_n()

    sent_id = 0 # Id sequence for sentence-id
    sent_dict = {}
    with open('./data/out/topic{}_doc_ids'.format(topic_id), 'w', encoding='utf-8') as f:
        for (doc, score) in doc_list:
            f.write(doc.id + '\t' + str(score) + '\n')
            for sent in doc.sent_list:
                s = Sentence(sent_id, doc.id, sent)
                sent_dict[sent_id] = s
                sent_id += 1

    """ Sentence graph that will contain edges between sentences """
    sent_graph = Graph(term_dict)

    for sent in sent_dict:
        sent_graph.add_node(Node(sent_dict[sent]))

    
    sent_graph.create_graph() # The edges are created

    """ The adjaceny matrix for sentences which conducts PageRank  """
    sent_rank = DocRank(sent_graph)

    """ List of most rated 20 sentences """
    sent_list = sent_rank.return_max_n(n=20)

    with open('./data/out/topic{}_sentences'.format(topic_id), 'w', encoding='utf-8') as f:
        f.write(topic_details[topic_id].question + '\n\n')
        for (sent, score) in sent_list:
            f.write(sent.text + '\t' + str(score) + '\n')


if __name__ == "__main__":

    all_docs = parse.read_relevance_doc()

    topic_details = parse.read_topic_doc()

    if sys.argv[1] == '-h':
        for topic in topic_details:
            print(f"{topic}\t{topic_details[topic].query}")
    else:
        for arg in sys.argv[1:]:
            id = int(arg)
            query = topic_details[id].query
            print("Summarizing \"{}\" related papers...".format(query))
            get_summary_sentences(id)