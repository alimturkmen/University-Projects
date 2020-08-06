import re

class Preprocess(object):

    def __init__(self):
        self.stopwords = []

    # Reads a file and return the tokenized form of it
    # If needed, stop-words are removed
    def read_norm_file(self, path, remove_stop_words=True):
        self.stopwords = []
        if remove_stop_words:
            stopwords = self.tokenizer(open('stop_words', 'r').read())
            self.stopwords = stopwords
        data = open(path, 'r').read()
        return self.tokenizer(data)

    # Reads the files in a given directory.
    # Returns a list of lists of tokens. 
    # It is possible to combine all of the documents into a one.
    def read_norm_multifile(self, path, remove_stop_words=True, combine_files=False):
        import os

        self.stopwords = []
        if remove_stop_words:
            stopwords = self.tokenizer(open('stop_words', 'r').read())
            self.stopwords = stopwords

        files = [f for f in os.listdir(path,) if (os.path.isfile(os.path.join(path, f)) and f[0] != '.')]
        if combine_files:
            all_in_one = ''
            for f in files:
                all_in_one += open(path+f, 'r').read()
            data = all_in_one
            tokens = [self.tokenizer(data)]
            labels = [1]  if path[-4:-1]=='pos' else [0]
        else:
            tokens = []
            cls=1 if path[-4:-1]=='pos' else 0
            labels = []
            for f in files:
                doc = open(path+f, 'r').read()
                tokenized_doc = self.tokenizer(doc)
                tokens.append(tokenized_doc)
                labels.append(cls)

        return tokens, len(files), labels   

    # Splits a text by spaces and punctuations. 
    # Tokens can be thought as words.
    # Words are lowercased
    # Clitics are replaced with corresponding word.
    def tokenizer(self, str):
        str += ' '
        words = [] #list of words
        word = ''

        for char in str:
            if char in [' ', '.', ',', '?', '!', ':', '\n', '\"', '(', ')', '[', ']', '/', '\\', '<', '>']:
                word = self.case_folding(word)
                word, flag = self.replace_clitics(word)
                if flag:
                    word_temp = ''
                    for char in word:
                        if char == ' ':
                            if word_temp not in self.stopwords : words.append(word_temp)
                            word_temp = ''
                        else: word_temp += char
                    if word_temp not in self.stopwords : words.append(word_temp)
                elif word not in self.stopwords and word != '':
                    words.append(word)
                word = ''      
            else:
                word += char
        
        return words

    # Turns a given text into lowercase
    def case_folding(self, word):

        char_set = {'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e', 
                    'F':'f', 'G':'g', 'H':'h', 'I':'i', 'J':'j', 'K':'k', 
                    'L':'l', 'M':'m', 'N':'n', 'O':'o', 'P':'p', 'Q':'q', 
                    'R':'r', 'S':'s', 'T':'t', 'V':'v', 'U':'u', 'X':'x', 
                    'Y':'y', 'Z':'z', 'W':'w'}
        word_lower = ''

        if re.search('.*[A-Z].*', word):
            word_lower = ''
            for char in word:
                if char in char_set.keys():
                    char = char_set[char]
                word_lower += char
            word = word_lower
       
        return word

    # Replaces clitics with regarding words.
    # Returns error message if an undefined clitic is given
    def replace_clitics(self, word):
        #Clitic set that is used to replace clitics with regarding words.
        clitic_set = {
            'll' : 'will',
            'm' : 'am',
            're' : 'are',
            'd' : 'would',
            've' : 'have',
            't' : 'not',
            's' : 's'
        }

        clitic = 'none'
        word_proc = ''

        for idx, char in enumerate(word):
            if clitic != 'none':
                clitic += char

            if char == '\'':
                clitic = ''
                word_proc = word[0:idx]
        flag = False
        if clitic != 'none':
            if clitic in clitic_set.keys():
                word = word_proc if clitic != 't' else word_proc[0:-1]
                word += ' ' + clitic_set[clitic]
                flag = True
            else:
                word = word_proc + '\'' + clitic

        return word, flag