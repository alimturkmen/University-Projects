from os import listdir
from os.path import isfile, join
import os
from collections import Counter
import math
import sys
 
try:
    TRAINING_PATH = sys.argv[1] #Path of the training files
    TEST_PATH = sys.argv[2] #Path of the test files
    USE_STOPWORDS = sys.argv[3] #Eliminate stopwords or not in processing 
    if USE_STOPWORDS == 'False':
        USE_STOPWORDS = False
    WEIGHTING = sys.argv[4] #The weighting algorithm 
    THRESHOLD = int(sys.argv[5]) #The threshold for counting the word occurences 
    WRITE_TO_FILE = sys.argv[6] #Write the output of training to a file or not
    if WRITE_TO_FILE == 'False':
        WRITE_TO_FILE = False 
except :
    print("Given missing arguements...\nUsing default values...")
    pwd = os.getcwd()
    TRAINING_PATH = pwd+'/articles/training/'
    TEST_PATH = pwd+'/articles/test/'
    USE_STOPWORDS = False
    WEIGHTING = 'tf'
    THRESHOLD = 4
    WRITE_TO_FILE = False

stopwords = open('stopwords.txt','r').read().split('\n') #The stopwords list

# Removes punctuations and other non alpha-numeric characters.
def remove_punctuation(text):
    text = text.replace('\'', ' ').replace('\n', ' ').replace('.', '').replace(',', '').replace('*', '').replace('/', ' ')
    text = text.replace('?', '').replace('(', '').replace(')', '').replace(':', '').replace(';', '').replace('’', ' ')

    return text

# Reads the all of the files in the given directory. 
# Stopwords are eliminated from the corpus according to user's choice. 
# The docs in the files are read and put into a list. 
# Regarding labels are also kept in a list and these are returned.
def read_file(path, use_stopwords=True):
    
    global stopwords

    files = [f for f in listdir(path,) if isfile(join(path, f))]
    labels_set = {'m':0, 't':1, 's':2} #movie:0, theatre:1, sport:2
    articles = []
    labels = []
    vocab_set = []

    for file in files:
        file_path = path+file
        article_raw = open(file_path, 'r').read()
        article_raw = remove_punctuation(article_raw)
        article_raw=article_raw.lower().split(' ')
        article_processed = []

        for word in article_raw:
            if use_stopwords:
                if word not in stopwords:
                    if word not in vocab_set:
                        vocab_set.append(word)
                    article_processed.append(word)
            else:
                if word not in vocab_set:
                    vocab_set.append(word)
                article_processed.append(word)

        articles.append(article_processed)
        labels.append(labels_set[file[0]])

    return articles, labels, vocab_set

# Calculates the inverse-document-frequencies of the words in given document list.
def inverse_frequency(x):
    number_of_documents = len(x)
    word_inv_freq = {}

    for xi in x:
        x_counter = Counter(xi)
        for word in x_counter.keys():
            if word in word_inv_freq:
                word_inv_freq[word] += 1
            else:
                word_inv_freq[word] = 1
    
    for word in word_inv_freq.keys():
        word_inv_freq[word] = number_of_documents/word_inv_freq[word]

    return word_inv_freq

# Takes tf and idf to calculate tf-idf weighting of words in the corpus.
def calc_tf_idf(inverse_frequency, word_counts):

    for clss in range(len(word_counts)):
        for word in word_counts[clss]:
            word_counts[clss][word] = word_counts[clss][word]*inverse_frequency[word]

    return word_counts

# Trains the naive bayes classifier using the given weighting algorithm.
# Returns word counts of classes, overall word counts and document counts.
def train(x, y, threshold=None, weighting='tf'):
    
    number_of_classes = len(set(y))
    training_matrix = {} # Set of all articles with their words in beloning classes
    word_counts = [] # Word occurence list among classes
    document_count = {} # Set of document counts in belonging classes

    for i in range(0, number_of_classes):
        training_matrix[i] = [] 
        document_count[i] = 0
        word_counts.append({})

    for idx, xi in enumerate(x):
        training_matrix[y[idx]].extend(xi)
        document_count[y[idx]] += 1

    if weighting == 'tf' or weighting == 'tf-idf':

        total_word_count = []
        for i in range(0, number_of_classes):
            word_counts[i] = Counter(training_matrix[i])
            total_word_count.extend(training_matrix[i])
        
        total_word_counts = Counter(total_word_count)
        if threshold:
            temp_word_counts = [{}, {}, {}]
            temp_total_word_counts = {}
            for word in total_word_count:
                if total_word_counts[word] > threshold:
                    temp_total_word_counts[word] = total_word_counts[word]
                    if word in word_counts[0].keys():
                        temp_word_counts[0][word] = word_counts[0][word]
                    if word in word_counts[1].keys():
                        temp_word_counts[1][word] = word_counts[1][word]
                    if word in word_counts[2].keys():
                        temp_word_counts[2][word] = word_counts[2][word]
                    
            total_word_counts = temp_total_word_counts
            word_counts = temp_word_counts

        if weighting == 'tf-idf':
            inv_freq = inverse_frequency(x)
            word_counts = calc_tf_idf(inv_freq, word_counts)


    elif weighting == 'binary':

        total_word_counts = {}
        for i in range(0, number_of_classes):
            for word in training_matrix[i]:
                if word not in word_counts[i].keys():
                    word_counts[i][word] = 1
                    if word not in total_word_counts.keys():
                        total_word_counts[word] = 1
                    else:
                        total_word_counts[word] = total_word_counts[word] + 1

        if threshold:
            temp_word_counts = [{}, {}, {}]
            temp_total_word_counts = {}
            for word in total_word_counts.keys():
                if total_word_counts[word] > threshold:
                    temp_total_word_counts[word] = total_word_counts[word]
                    if word in word_counts[0].keys():
                        temp_word_counts[0][word] = word_counts[0][word]
                    if word in word_counts[1].keys():
                        temp_word_counts[1][word] = word_counts[1][word]
                    if word in word_counts[2].keys():
                        temp_word_counts[2][word] = word_counts[2][word]
                    
            total_word_counts = temp_total_word_counts
            word_counts = temp_word_counts

    else: 
        print("Given unrecognized weighting. It can be 'tf', 'binary' or 'tf-idf'")
        sys.exit(1)
    return word_counts, total_word_counts, document_count

# Tests the trained model with the fiven files. 
def test(x, y, word_counts, total_word_count, document_count):

    predictions = [] # Keeps the max-probability results of given documents
    number_of_types = len(total_word_count.keys()) 
    number_of_docs = sum(document_count.values())
    unseen_words = []

    for xi in x:
        probs = [] # List of all classes' scores
        for i in document_count.keys():
            p_word_d = 1.0 # p(w|d)
            for word in xi:
                if word not in total_word_count.keys():
                    unseen_words.append(word)
                if word in word_counts[i].keys():
                    p_word_d += math.log((word_counts[i][word]+1)/(sum(word_counts[i].values())+number_of_types))
                else:
                    p_word_d += math.log((1.0)/(sum(word_counts[i].values())+len(total_word_count.keys())))
                
            p_d =  math.log(document_count[i]/number_of_docs) #p(d)
            probability = p_d + p_word_d 
            probs.append(probability)
        
        predictions.append(probs.index(max(probs)))
    
    return predictions, set(unseen_words)

# Creates confusion matrix of the model's results. 
def create_confusion_matrix (predictions, y):
    number_of_classes = len(set(y))
    confusion_matrix = []
    for i in range(number_of_classes):
        new_row = []
        for j in range(number_of_classes):
            new_row.append(0)
        confusion_matrix.append(new_row)
    
    for index in range(len(y)):
        confusion_matrix[predictions[index]][y[index]] += 1
    
    return confusion_matrix

# Calculates macro-average precision, recall and f1 scores.
def calc_macro_metrics(predictions, y):
    confusion_matrix = create_confusion_matrix(predictions, y)
    number_of_classes = len(set(y))
    macro_metrics = {}
    precision, recall = 0, 0

    for i in range(number_of_classes):
        sum_precision = 0
        sum_recall = 0
        for j in range(number_of_classes):
            sum_precision += confusion_matrix[i][j]
            sum_recall += confusion_matrix[j][i]
        if sum_precision != 0:
            precision += confusion_matrix[i][i]/sum_precision
        else:
            precision = 0
        if sum_recall != 0:
            recall += confusion_matrix[i][i]/sum_recall
        else:
            recall = 0

    precision = precision/3
    recall = recall/3
    macro_metrics['precision'] = precision
    macro_metrics['recall'] = recall
    if  precision+recall != 0:
        macro_metrics['f1'] = 2*recall*precision/(precision+recall)
    else:
        macro_metrics['f1'] = 0

    return macro_metrics

# Calculates micro-average precision, recall and f1 scores.
def calc_micro_metrics(predictions, y):

    confusion_matrix = create_confusion_matrix(predictions, y)
    number_of_classes = len(set(y))
    micro_metrics = {}
    precision, recall = 0, 0
    sum_precision = 0
    sum_recall = 0
    for i in range(number_of_classes):
        for j in range(number_of_classes):
            sum_precision += confusion_matrix[i][j]
            sum_recall += confusion_matrix[j][i]
        precision += confusion_matrix[i][i]
        recall += confusion_matrix[i][i]

    if sum_precision != 0:
        precision = precision/sum_precision
    else:
        precision = 0
    if sum_recall != 0:
        recall = recall/sum_recall
    else:
        recall = 0
    micro_metrics['precision'] = precision
    micro_metrics['recall'] = recall
    if (precision+recall) != 0:
        micro_metrics['f1'] = 2*precision*recall/(precision+recall)
    else:
        micro_metrics['f1'] = 0

    return micro_metrics

x_train,y_train,_ = read_file(TRAINING_PATH, use_stopwords=USE_STOPWORDS)
word_counts, total_word_count, document_count = train(x_train, y_train, threshold=THRESHOLD, weighting=WEIGHTING)

if WRITE_TO_FILE:
    file_word_count = open('word_counts.txt', 'w')
    file_word_count.write(str(word_counts))
    file_total_word_count = open('total_word_counts.txt', 'w')
    file_total_word_count.write(str(total_word_count))
    file_doc_count = open('doc_counts.txt', 'w')
    file_doc_count.write(str(document_count))

x_test,y_test,_ = read_file(TEST_PATH, use_stopwords=USE_STOPWORDS)
predictions, unseen_words = test(x_test, y_test, word_counts, total_word_count, document_count)

micro = calc_micro_metrics(predictions, y_test)
macro = calc_macro_metrics(predictions, y_test)

print('___________\n')
print('PARAMETERS')
print('___________\n')
print('Weighting: '+ WEIGHTING)
print('Threshold: ' + str(THRESHOLD))
print('Clean stopwords: ' + str(USE_STOPWORDS))
print('Number of features:' + str(len(total_word_count.keys())))
print('Number of unseen words: '+ str(len(unseen_words)))
#print('Unseen words: '+ str(unseen_words))
print('___________\n')
print('RESULTS')
print('___________\n')
print('True labels: '+str(y_test))
print('Predicted labels: ' + str(predictions))
print('___________\n')
print('EVAULATION')
print('___________')
print('micro-average scores: ' + str(micro))
print('macro-average scores: ' + str(macro))
