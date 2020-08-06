import math
from evaluation import Evaluate

# Class of Naive Bayes Model
# Enables you to train, test and evaluate the models
class NaiveBayes(object):

    def __init__(self, type='Multinomial'):
        self.type = type # Multinomial, Bernoulli or Binary
        self.doc_counts = {} # Stores number of documents for each class
        self.num_of_docs = 0 # Stores total number of all documents
        self.word_counts = {} # Stores number of each word's frequency (based on nb type) for each class
        self.total_word_counts = {} # Stores total number of words in each class
        self.num_of_dis_words = {} # Stores number of distinct words for each class

    # Training part
    # The initial setup is performed
    # The data to be trained is passed to other functions according to model type
    def train(self, data, labels, doc_counts=None, smoothing=False):
        doc_count_flag = True
        self.smoothing = smoothing
        # If the document counts are not given by the user, count documents manually
        if doc_counts : 
            self.doc_counts = doc_counts
            for i in doc_counts.keys():
                self.num_of_docs += doc_counts[i]
            doc_count_flag = False
        # Number of classes in the dataset
        self.num_of_cls = max(labels) + 1

        if self.type=='Multinomial':
            self.train_MNB(data, labels, doc_count_flag, smoothing)
        elif self.type=='Bernoulli':
            self.train_BNB(data, labels, doc_count_flag, smoothing)
        else:
            self.train_bin(data, labels, doc_count_flag, smoothing)
            
    # Multinomial NB - training part
    # The necessary datastructures are initiated.
    # Documents are read one by one and words' frequencies are counted.
    # Smoothing is applied in this part, if it is needed.
    def train_MNB(self, data, labels, doc_count_flag, smoothing):
        alpha = 1 if smoothing else 0

        for i in range(0, self.num_of_cls):
            self.word_counts[i]={}
            self.total_word_counts[i] = 0
            self.num_of_dis_words[i] = 0
            if doc_count_flag : self.doc_counts[i] = 0

        for idx, doc in enumerate(data):
            cls = labels[idx]
            if doc_count_flag : self.doc_counts[cls] += 1
            if doc_count_flag : self.num_of_docs += 1

            for token in doc:
                if token in self.word_counts[cls].keys():
                    self.word_counts[cls][token] += 1
                    if self.word_counts[cls][token] == alpha : self.num_of_dis_words[cls] += 1
                else : 
                    self.word_counts[cls][token] = 1 + alpha
                    self.num_of_dis_words[cls] += 1
                self.total_word_counts[cls] += 1
                for i in range(0, self.num_of_cls):
                    if cls != i:
                        if token not in self.word_counts[i].keys() : 
                            self.word_counts[i][token] = alpha
                            self.num_of_dis_words[i] += alpha
        
        for c in range(0, self.num_of_cls):
            self.total_word_counts[c] += self.num_of_dis_words[c]*alpha

    # Bernoulli NB - training part
    # The necessary datastructures are initiated.
    # Number of documents containing each word are counted and stored.
    # Smoothing is applied in this part, if it is needed.
    def train_BNB(self, data, labels, doc_count_flag, smoothing):
        alpha = 1 if smoothing else 0

        for i in range(0, self.num_of_cls):
            self.word_counts[i]={}
            self.total_word_counts[i] = 0
            self.num_of_dis_words[i] = 0
            if doc_count_flag : self.doc_counts[i] = 0

        for idx, doc in enumerate(data):
            cls = labels[idx]
            if doc_count_flag : self.doc_counts[cls] += 1
            if doc_count_flag : self.num_of_docs += 1

            token_list = []
            for token in doc:
                if token not in token_list:
                    if token in self.word_counts[cls].keys() : self.word_counts[cls][token] += 1
                    else:
                        self.word_counts[cls][token] = 1 + alpha
                    for i in range(0, self.num_of_cls):
                        if cls != i:
                            if token not in self.word_counts[i].keys() : self.word_counts[i][token] = alpha
                token_list.append(token)

        for c in range(0, self.num_of_cls):
            self.total_word_counts[c] = self.doc_counts[i]+2*alpha

    # Binary NB - training part
    # The necessary datastructures are initiated.
    # If a word occurs in class it is counted once.
    # Smoothing is applied in this part, if it is needed.    
    def train_bin(self, data, labels, doc_count_flag, smoothing):    
        alpha = 1 if smoothing else 0

        for i in range(0, self.num_of_cls):
            self.word_counts[i]={}
            self.total_word_counts[i] = 0
            self.num_of_dis_words[i] = 0
            if doc_count_flag : self.doc_counts[i] = 0

        for idx, doc in enumerate(data):
            cls = labels[idx]
            if doc_count_flag : self.doc_counts[cls] += 1
            if doc_count_flag : self.num_of_docs += 1

            for token in doc:
                if token not in self.word_counts[cls].keys() : 
                    self.word_counts[cls][token] = 1 + alpha
                    self.num_of_dis_words[cls] += 1
                    self.total_word_counts[cls] += 1
                elif self.word_counts[cls][token] == alpha:
                    self.word_counts[cls][token] += 1
                    self.total_word_counts[cls] += 1
                for i in range(0, self.num_of_cls):
                    if cls != i:
                        if token not in self.word_counts[i].keys() : 
                            self.word_counts[i][token] = alpha
                            self.num_of_dis_words[i] += 1*alpha
        
        for c in range(0, self.num_of_cls):
            self.total_word_counts[c] += (self.num_of_dis_words[c]*alpha)

    # The trained model can be saved by using this function.
    # Stores word occurences of each classes
    def save_model(self, file_name):
        w_file = open(file_name, 'w')
        w_file.write('doc_count\n')
        for cnt in self.doc_counts.keys():
            w_file.write(str(cnt)+':'+str(self.doc_counts[cnt])+'\n')
        w_file.write('\n')
        w_file.write('word_counts\n')
        for cnt in self.word_counts.keys():
            w_file.write(str(cnt)+':\n')
            for word in self.word_counts[cnt].keys():
                w_file.write(word+':'+str(self.word_counts[cnt][word])+'\n')
            w_file.write('\n')
        
    # For a given set of documents,
    #   finds each document's class
    #   evaluates the models score for this test set
    #   returns a list of predictions made for each document and the scores of the model.
    def test(self, data, labels):
        
        predictions = []
        cnt_correct = 0
        for idx, doc in enumerate(data):
            _, prediction = self.predict(doc)
            predictions.append(prediction)
            true_label = labels[idx]
            if true_label == prediction:
                cnt_correct += 1

        eval = Evaluate(predictions, labels, self.num_of_cls)
        metrics = {'macro':eval.calc_macro_metrics(), 'micro':eval.calc_micro_metrics()}
        return predictions, metrics

    # For a given document, predicts its class.
    # For zero probability cases to prevent log domain problems epsilon is added to numerator.
    # Returns log probability scores and predicted class.
    def predict(self, doc):
        
        smoothing = self.smoothing
        epsilon =  0.001
        probs = {}
        max_prob = -math.inf
        arg_max_cls = 0

        if self.type == 'Bernoulli':
            for cls in range(self.num_of_cls):
                p_c = math.log(self.doc_counts[cls] / self.num_of_docs)
                p_w_c = 0
                p_w_c_neg = 0
                token_list = []
                for token in doc:
                    if token in self.word_counts[cls].keys():
                        if self.word_counts[cls][token]==0:
                            p_w_c += math.log((self.word_counts[cls][token]+epsilon)/(self.total_word_counts[cls]))
                        else :
                            p_w_c += math.log((self.word_counts[cls][token])/(self.total_word_counts[cls]))
                    else:
                        if smoothing:
                            p_w_c += math.log(1.0/self.total_word_counts[cls])
                        else:
                            p_w_c += math.log(epsilon/self.total_word_counts[cls])
                    token_list.append(token)
                
                for feature in self.word_counts[cls].keys():
                    p = 0
                    if feature not in token_list:
                        p = math.log(1-self.word_counts[cls][feature]/(self.total_word_counts[cls]+epsilon))
                        p_w_c_neg += p

                prob = p_c + p_w_c + p_w_c_neg
                if prob > max_prob:
                    max_prob = prob
                    arg_max_cls = cls
                probs[cls] = prob

        else:
            for cls in range(self.num_of_cls):
                p_c = math.log(self.doc_counts[cls] / self.num_of_docs)
                p_w_c = 0
                for token in doc:
                    if token in self.word_counts[cls].keys():
                        if self.word_counts[cls][token] == 0:
                            p_w_c += math.log((self.word_counts[cls][token]+epsilon)/self.total_word_counts[cls])
                        else:
                            p_w_c += math.log((self.word_counts[cls][token])/self.total_word_counts[cls])
                    else:
                        if smoothing:
                            p_w_c += math.log(1.0/self.total_word_counts[cls])
                        else:
                            p_w_c += math.log(epsilon/self.total_word_counts[cls])
                prob = p_c+p_w_c

                if prob > max_prob:
                    max_prob = prob
                    arg_max_cls = cls

                probs[cls] = prob

        return probs, arg_max_cls

    # Randomization Test
    # Given a model pair and correct labels the randomization test is performed
    # Test is done for F score. 
    # F score of models are calculated by Evaluation object.
    def randomization_test(self, labels, y1, y2, epoch=1000):
        import random
        
        e = Evaluate(labels, y1, self.num_of_cls)
        f_1 = e.calc_micro_metrics()['f1']
        e = Evaluate(labels, y2, self.num_of_cls)
        f_2 = e.calc_micro_metrics()['f1']

        s = abs(f_1-f_2)
        cnt = 0
        for i in range(0, epoch):
            temp_y1 = []
            temp_y2 = []
            for idx in range(len(labels)):
                if random.uniform(0, 1) > 0.5:
                    temp_y1.append(y2[idx])
                    temp_y2.append(y1[idx])
                else:
                    temp_y1.append(y1[idx])
                    temp_y2.append(y2[idx])
            
            e = Evaluate(labels, temp_y1, self.num_of_cls)
            f_1 = e.calc_micro_metrics()['f1']
            e = Evaluate(labels, temp_y2, self.num_of_cls)
            f_2 = e.calc_micro_metrics()['f1']
            s_prime = abs(f_1-f_2)

            if s_prime > s:
                cnt += 1

        p_value = (cnt+1)/(epoch+1)

        return p_value
            
