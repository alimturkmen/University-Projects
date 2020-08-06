This is a basic summarization system which is based on PageRank algorithm.

In order to run the program, be sure that you have python 3.7 or higher. You also need nltk module and its stopwords corpus. (You can download it with running `nltk.download('stopwords')` on a python console.)

*main.py* is the code-piece that you should run. Normally, it is designed for summarizaiton of papers for a given topic-id but you can also give a list of ids. i.e.
`python main.py 5` or `python main.py 1 3 7`
If you want to see the topics just run `python main.py -h`

The program needs a __data__ directory which includes 

- *metadata.csv* which has the abstracts of the papers and other metadata
- *relevance.txt*, containing relevance-judgements of papers 
- *topics.xml* that stores the metadata of topics

otherwise change the respective parts in the code. 

After executing *main.py* by giving topic id parameters, the document-ids that have highest PageRank scores are listed in a file which is located in __./data/out/__ directory. Also, the sentences that is thought to be the summary of the topic are written in a file in the same directory.

__Folder Structure__

	|-- data
        |-- out
            |-- topic1_doc_ids
            |-- topic1_sentences
            ...
        |-- metadata.csv
        |-- relevance.txt
        |-- topics.xml
	|-- main.py
	|-- doc_rank.py
	|-- functions.py
	|-- parse.py
	|-- vectorize.py
	|-- entities.py					
	|-- README.md


You can read Docstrings of modules or check them out after importing. (i.e. `help()`)