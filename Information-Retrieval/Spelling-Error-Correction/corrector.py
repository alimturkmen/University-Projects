# The global char dictionary which is used to map characters to numbers.
chars_with_idx ={'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 
    'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 
    'l':11, 'm':12, 'n':13, 'o':14, 'p':15, 'q':16, 
    'r':17, 's':18, 't':19, 'u':20, 'v':21, 'w':22, 
    'x':23, 'y':24, 'z':25, '\'':26, '-':27, '_':28, '':29}

# Splits a text by spaces and punctuations. 
# Tokens can be thought as words.
def tokenizer(str):
    str += ' '
    words = [] #list of words
    word = ''
    for idx, char in enumerate(str):
        if char in [' ', '.', ',', '?', '!', ':', '\n', '\'', '\"', '(', ')', '[', ']', '/', '\\', '<', '>']:
            if not (char == '\'' and (str[idx+1] == ' ' or str[idx-1] == ' ') ) :
                words.append(word)
                word = ''      
        else:
            word += char
    
    return words


# Tokenizes the given text.
# Removes punctuations and returns the lowercased tokens.
def preprocess(txt):
    #This char_set is used to turn a text into lowercase.
    char_set = {'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e', 
    'F':'f', 'G':'g', 'H':'h', 'I':'i', 'J':'j', 'K':'k', 
    'L':'l', 'M':'m', 'N':'n', 'O':'o', 'P':'p', 'Q':'q', 
    'R':'r', 'S':'s', 'T':'t', 'V':'v', 'U':'u', 'X':'x', 
    'Y':'y', 'Z':'z', 'W':'w'}
    
    import re
    words = tokenizer(txt)
    changed_words = {} #dictionary that stores the original words and the uppercase-version of them
    txt_lower = [] #stores tokens

    for word in words:
        if re.search('.*[A-Z].*', word):
            word_lower = ''
            for char in word:
                if char in char_set.keys():
                    char = char_set[char]
                word_lower += char
            changed_words[word] = word_lower
            word = word_lower
        txt_lower.append(word)
    
    #print(" >> Corpus is tokenized successfully.")
    return txt_lower, changed_words


# Creates the counter dictionary.
# Counts the occurences of each word.
# Returns word-count dictionary, number of distinct words and number of all words in the corpus.
def create_dict(file_name):
    corpus = open('corpus.txt', 'r').read()
    tokenized_corpus, _ = preprocess(corpus)
    counter = {}
    dist_words = 0
    total_words = len(tokenized_corpus)

    for token in tokenized_corpus:
        if token != '':
            if token in counter.keys():
                counter[token] += 1
            else:
                counter[token] = 1
                dist_words += 1

    print(f" >> Word-count dictionary is created with {dist_words} distincts words")
    return counter, dist_words, total_words


# Return default confusion matrix of del, ins, sub and trans operations.
# If user choses Laplace smoothing matrices created with ones otherwise with zeroes.
def create_conf_matrices():
    global SMOOTHING

    def_list1, def_list2, def_list3, def_list4 = [], [], [], []
    for _ in range(30):
        ll1, ll2, ll3, ll4 = [], [], [], []
        for _ in range(30):
            if SMOOTHING:
                ll1.append(1)
                ll2.append(1)
                ll3.append(1)
                ll4.append(1)
            else:
                ll1.append(0)
                ll2.append(0)
                ll3.append(0)
                ll4.append(0)
        def_list1.append(ll1)
        def_list2.append(ll2)
        def_list3.append(ll3)
        def_list4.append(ll4)

    conf_matrices = {'del':def_list1, 'ins':def_list2, 'sub':def_list3, 'trans':def_list4}

    return conf_matrices


# Finds the type of the edit operation.
# Returns edit type, edit character and previous character.
# Only considers the edit operations with 1 edit distance.
# If the edit distance is more than one return None for all parameters
# x is the mispelled word and y is the corrected form of x.
def calc_distance(x, y):
    
    global chars_with_idx
    
    x = preprocess(x)[0][0] # normalization
    y = preprocess(y)[0][0] # normalization

    edit_type, correct, error = None, None, None
    
    if len(x) == len(y) + 1:    #gets here if x is 1 insert-distant to y
        for idx, char in enumerate(y):
            if (x[idx] != char and x[idx+1:] == y[idx:]) or idx==len(y)-1:
                edit_type = 'ins'
                if idx == len(y)-1:
                    error = y[idx]
                    correct = x[idx+1]
                else:
                    error = y[idx-1]
                    correct = x[idx]
                break
    elif len(y) == len(x) + 1:  #gets here if x is 1 deletion-distant to y
        for idx, char in enumerate(x):
            if (y[idx] != char and x[idx:] == y[idx+1:]) or idx==len(x)-1 :
                edit_type = 'del'
                if idx == 0:
                    correct = y[idx]
                    error = ''
                else:
                    correct = y[idx+1]
                    error = char
                break
    elif len(x) == len(y):
        for idx, char in enumerate(y):
            if char != x[idx] and (x[idx+1:]==y[idx+1:] or idx == len(x)-1): #gets here if x is 1 substitution-distant to y
                edit_type = 'sub'
                correct = char
                error = x[idx]
                break
            elif char != x[idx] and x[idx+1] == char and x[idx] == y[idx+1] and (x[idx+2:]==y[idx+2:] or idx == len(x)-2):
                #gets here if x is 1 transposition-distant to y
                edit_type = 'trans'
                error = char
                correct = x[idx]
                break
    
    if edit_type!=None:
        return edit_type, chars_with_idx[error], chars_with_idx[correct]
    else:
        return None, None, None
    

# Fills the 4 confusion matrices with given spelling-errors file.
# Return the confusion matrices.
def create_err_dict(file_name):

    err_corpus = open(file_name, 'r').read()
    conf_matrices = create_conf_matrices()
    colon_flag = False #Another misspelled word
    newline_flag = True #End of misspelled words for current word
    num_flag = False #Misspelled word occurs more than once
    key = ''  #Refers to the correct word
    value = '' #Refers to the misspelled forms

    for char in err_corpus:
        if newline_flag:
            if char == ':':
                colon_flag = True
                newline_flag = False
            else:
                key += char
        if colon_flag:
            if char != ' ' and char != ':':
                if char == '*':
                    num_flag = True
                elif char == ',' or char == '\n':
                    if num_flag:
                        num_flag = False
                        edit_type, err, corr = calc_distance(value, key)
                        if edit_type != None:
                            conf_matrices[edit_type][err][corr] += freq
                    else:
                        edit_type, err, corr = calc_distance(value, key)
                        if edit_type != None:
                            conf_matrices[edit_type][err][corr] += 1
                    value = ''
                    if char == '\n':
                        newline_flag=True
                        colon_flag = False
                        key = ''
                elif num_flag:
                    freq = int(char)
                else: 
                    value += char
    return conf_matrices


# Writes confusion matrices to seperate files.
def write_conf_matrices(matrix):
    global chars_with_idx

    for typ in matrix.keys():
        f = open(typ, 'w')
        f.write('\t')
        for ch in chars_with_idx.keys():
            f.write(ch + '\t')
        f.write('\n')
        for i in range (30):
            f.write(str(list(chars_with_idx.keys())[i])+'\t')
            for j in range(30):
                f.write(str(matrix[typ][i][j])+'\t')
            f.write('\n')

# Returns the denominators of each p(x|w) values for each edit operation.
def calc_denom(conf_matrices):

    all_denoms = []
    for idx, key in enumerate(conf_matrices.keys()):
        ll = []
        for i in range(30):
            sum = 0
            for j in range(30):
                sum += conf_matrices[key][i][j]
            ll.append(sum)
        all_denoms.append(ll)

    return all_denoms

# Generates the words with 1 edit-distant to given word.
# Only selects the words which are in the given dictionary.
def generate_words(word, dictionary):
    global chars_with_idx

    del_words, del_idx = [], [] #Stores words obtained from deletion and the edit characters
    ins_words, ins_idx = [], [] #Stores words obtained from insertion and the edit characters
    sub_words, sub_idx = [], [] #Stores words obtained from substitution and the edit characters
    trans_words, trans_idx = [], [] #Stores words obtained from transposition and the edit characters

    if len(word) != 0:
        for i in range(len(word)+1):
            for char in chars_with_idx.keys():
                new_word = word[0:i] + char + word[i:]
                if new_word in dictionary:
                    if i == len(word):
                        x=word[i-1]
                    else:
                        x = word[i]
                    y = char
                    del_words.append(new_word)
                    del_idx.append((chars_with_idx[x],chars_with_idx[y]))
        for i in range(len(word)):
            new_word = word[0:i]+word[i+1:]
            if new_word in dictionary:
                x = word[i-1]
                y = word[i]
                ins_words.append(new_word)
                ins_idx.append((chars_with_idx[x],chars_with_idx[y]))
        for i in range(len(word)):
            for char in chars_with_idx.keys():
                if char != '':
                    new_word = word[0:i]+char+word[i+1:]
                    if new_word in dictionary:
                        x = word[i]
                        y = char
                        sub_words.append(new_word)
                        sub_idx.append((chars_with_idx[x],chars_with_idx[y]))
        for i in range(len(word)-1):
            new_word = word[0:i] + word[i+1] + word[i] + word[i+2:]
            if new_word in dictionary:
                x = word[i+1]
                y = word[i]
                trans_words.append(new_word)
                trans_idx.append((chars_with_idx[x],chars_with_idx[y]))

    return del_words, ins_words, sub_words, trans_words, del_idx, ins_idx, sub_idx, trans_idx

# Calculates the error probability of each word generated in generate_words() function.
# Returns all of the probabilities of words in the given word list.
# Also returns the word having maximum likelihood and its index.
def calculate_prob(words, word_count, conf_matrix, idx, denom, total_words):
    if len(words)==0:
        return False

    word_probs = []
    max_prob = 0
    max_index = 0

    for index, word in enumerate(words):
        
        prob = word_count[word]/total_words
        prob*= int(conf_matrix[idx[index][0]][idx[index][1]])/denom[idx[index][0]]
        word_probs.append(prob)
        if prob > max_prob:
            max_prob = prob
            max_index = index

    return {'probs':word_probs, 'max_index':max_index, 'max_prob':max_prob}

# Takes misspelled words and returns the predicted ones for each word.
# Gets all of the predicted words obtained from edit operations for each misspelled word.
# Returns predictions only having maximum probability for corresponding misspelled word.
def predict_misspelled_words(word_count, total_words, conf_matrices, file_name):
    f = open(file_name, 'r').read()
    denoms = calc_denom(conf_matrices)
    del_denom, ins_denom, sub_denom, trans_denom = denoms[0], denoms[1], denoms[2], denoms[3]

    dictionary = word_count.keys()
    words = tokenizer(f)

    predicted_words=[]
    for word in words:

        # Each edit operation has different list for corrected words. 
        del_words, ins_words, sub_words, trans_words, del_idx, ins_idx, sub_idx, trans_idx = generate_words(word, dictionary)
        del_stats = calculate_prob(del_words, word_count, conf_matrices['del'], del_idx, del_denom, total_words)
        ins_stats = calculate_prob(ins_words, word_count, conf_matrices['ins'], ins_idx, ins_denom, total_words)
        sub_stats = calculate_prob(sub_words, word_count, conf_matrices['sub'], sub_idx, sub_denom, total_words)
        trans_stats = calculate_prob(trans_words, word_count, conf_matrices['trans'], trans_idx, trans_denom, total_words)
        
        edit_type = ''
        max_prob = 0

        if del_stats:
            edit_type='d'
            max_prob = del_stats['max_prob']

        if ins_stats:
            if ins_stats['max_prob'] > max_prob:
                max_prob = ins_stats['max_prob']
                edit_type='i'

        if sub_stats:
            if sub_stats['max_prob'] > max_prob:
                max_prob = sub_stats['max_prob']
                edit_type='s'

        if trans_stats:
            if trans_stats['max_prob'] > max_prob:
                max_prob = trans_stats['max_prob']
                edit_type='t'

        predicted_word = ''
        if edit_type == 'd':
            predicted_word = del_words[del_stats['max_index']]
        elif edit_type == 'i':
            predicted_word = ins_words[ins_stats['max_index']]
        elif edit_type == 's':
            predicted_word = sub_words[sub_stats['max_index']]
        elif edit_type == 't':
            predicted_word = trans_words[trans_stats['max_index']]
        predicted_words.append(predicted_word)

    return predicted_words

# Writes the predicted words
def write_to_file(word_list, file_name):
    wfile = open(file_name, 'w')
    wfile.write(word_list[0])
    for word in word_list[1:]:
        wfile.write('\n'+word)

# The main function of the program.
# Takes all of the necessary files and returns predicted correct form of misspelled words.
def correct_misspelled_words(corpus_file='corpus.txt', errors_file="spell-errors.txt", misspelled_file='test-words-misspelled.txt', output_file='predicted_words.txt'):
    word_count, _, total_words = create_dict(corpus_file)
    conf_matrices = create_err_dict(errors_file)
    write_conf_matrices(conf_matrices)
    predicted_words = predict_misspelled_words(word_count, total_words, conf_matrices, misspelled_file)
    write_to_file(predicted_words, output_file)
    
    return predicted_words

# Calculates the accuracy of corrections.
def calculate_accuracy(correct_words, predicted_words):
    correct_counter = 0
    empty_predictions = 0
    for i in range(len(correct_words)):
        if correct_words[i] == predicted_words[i]:
            correct_counter += 1
        elif predicted_words[i] == '':
            empty_predictions += 1

    return correct_counter/len(correct_words), empty_predictions/len(correct_words)

# Just reads the correct words.
def get_correct_words(file_name='test-words-correct.txt'):
    f = open(file_name, 'r').read()
    return tokenizer(f)


import sys

if len(sys.argv) < 4:
    print("Usage: python corrector.py [Laplace Smoothing Option] [Misspelled Word File] [Return Accuracy] [Correct Word File]")
    sys.exit(1)
else:
    SMOOTHING = (sys.argv[1] == 'True') #Laplace smoothing flag
    misspelled_words_file = sys.argv[2] 
    calc_accuracy = (sys.argv[3] == 'True') #Calculate accuracy flag
    predicted_words = correct_misspelled_words(misspelled_file=misspelled_words_file)
    if calc_accuracy:
        try:
            correct_words_file = sys.argv[4]
            correct_words = get_correct_words(correct_words_file)
            acc, empty_predictions = calculate_accuracy(correct_words, predicted_words)
            print(f"Accuracy: {acc} \t No prediction: {empty_predictions}")
        except:
            print("Missing or wrong correct word file.")
            sys.exit(1)