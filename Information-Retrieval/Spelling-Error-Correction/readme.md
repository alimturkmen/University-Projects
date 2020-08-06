Run program with:
python corrector.py [Laplace Smoothing Option(True/False)] [File of the misspelled words] [Calculate Accuracy(True/False)] [File of the correct words ]
Ex: python corrector.py True test-words-misspelled.txt True test-words-correct.txt
    python corrector.py False test-words-misspelled.txt False

Be sure you have python3.6 or higher version and corpus.txt and spell-errors.txt are located in the same directory. Also if you want the accuracy score, don't forget to give the path of the file with correct words.
