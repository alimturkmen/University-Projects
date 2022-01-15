import re
from termcolor import colored

#The message parameters. As it is understood from the names these are presented in the defined situtations.
WELCOME_MSG = "> Hi, welcome. I am CHATYAT. How can I help you?\n\
Please write your questions as gramatically correct as possible. Also please avoid misspelling and \
multiple questions in one sentence. :)"
NO_MATCH_ANSWER = "> I don't know the answer of your question. Is it possible that you misspelled something?"
DEFAULT_RESPONSE = "> I'm sorry, I do not understand your question. Please try it with different words. "
NOT_UNDERSTOOD_ANSWER = '> Sorry, I couldn\'t get your answer. Is it possible that you write something wrong? If you want to \
ask another question please write \'nq_\'.'

#This char_set is used to turn a text into lowercase.
char_set = {'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e', 
'F':'f', 'G':'g', 'H':'h', 'I':'i', 'J':'j', 'K':'k', 
'L':'l', 'M':'m', 'N':'n', 'O':'o', 'P':'p', 'Q':'q', 
'R':'r', 'S':'s', 'T':'t', 'V':'v', 'U':'u', 'X':'x', 
'Y':'y', 'Z':'z', 'W':'w'}

#Clitic set that is used to replace clitics with regarding words.
clitic_set = {
    'll' : 'will',
    'm' : 'am',
    're' : 'are',
    'd' : 'would',
    've' : 'have',
    't' : 'not'
}

#Meaning dictionary keeps the meaning of some words and abbreviations.
meanings = {
    'gpa': 'Grade Point Average',
    'spa': 'Semester Point Average',
    'repeat': 'the status of a student whose GPA is under 2.0 and whose SPA is also under 2.0 for two semesters',
    'graduation credits': '145',
    'senior': 'the student who have completed 108 credits',
    'senior student': 'the student who has completed 108 credits',
    'fourth grade': 'the student who has completed 108 credits',
    'irregular': 'the student starts the university in spring.'
}

# The main knowledgebase of the system. 
# Questions are detected by regular expressions and the regarding answer is generated.
# There are som sequences in the knowledge base. If a key starts with a number with underscore
# that means follows the key stated with that number. Similarly, if a key ends with underscore 
# and number that means it is the next sentence in the sequence. 
patterns = {
    r'.*what does (.+) (mean|stand for).*': 'It is # .', #1
    r'.*what is (.+).*': 'It is # .', #2
    r'.*need approval for (.+).*': 'Yes, you need approval from your advisor for # .', #3
    r'.*course from(.*school of.*)?applied science.*': 'No, you can\'t take credit course from school of applied sciences',
    r'.*(least|min|minimum) credits.*graduation.*': '145 credits.',
    r'.*reject.*': 'You should review your program and make changes on it. \
Don\'t forget to send it to approval before due date. Otherwise you have to register \
in late registration period and need to pay registration money.', #4
    r'.*(take|add) (5xx|cmpe 5.*).*': 'Which grade are you in?', #7
    r'^7_(4|fourth|4th|senior)(\w*)': 'What is your GPA?', #8
    r'^7_(1|2|3|third|3rd|first|1st|second|2nd|junior|freshman|sophomore)(\w*)': 'You need to be fourth grade to take 5xx courses.', #9
    r'(~\d)*(([0|1][\.|,])|(2[\.|,][0|1|2|3|4]))(\w*)_7$': 'No you can\'t. Your GPA should be greater than 2.5', #10
    r'.*((2[,|\.]([5|6|7|8|9])*)|(4[\.|,]0+)|(3[\.|,]\d*))_7$': 'Yes you can, then.', #11
    r'.*(drop|withdraw).*(course|cmpe).*': 'Which grade are you in?', #12
    r'^12_(1|first|freshman|1st)(\w)*': 'If you are an irregular student having GPA greater than 2.75 you can only change \
courses. Otherwise you cannot. In any ways your credits cannot go under 18', #13
    r'^12_(2|3|4|sophomore|senior|junior|second|third|fourth|4th|3rd|2nd)(\w*)': 'Do your total credits get under 18 when \
you drop/withdraw it or is this a course that you are repeating becaus of getting F?',
    r'(yes|yeap|unfortunately)_12$': 'Students\' taking 15 credits depends on the advisor\'s decision.\
it depends on the board\'s decision if it goes to 11. Also you can\'t drop or withdraw an F course.',
    r'(no|nope|not)_12$': 'Yes you can then. I hope it is the best for you :)',
    r'.*conflict.*': 'You should prepare a program without conflicts. If you have then it depends on your advisor.', #14
    r'.*(take|add) 6xx.*': 'No, undergrad students can\'t take 6xx courses.', #15
    r'.*nq_.*': "OK, I'm listening.", #16
    r'(hi|.*hello|hey).*': "Hi there.", #17
    r'.*(have|ask).*(question|problem).*': "Ok, please go on.", #18
    r'thank.*': "It is my pleasure. ", #19
    r'.*bye.*': "Bye"
}

# The index of sequence starting questions are stored in this list
sequences=[6, 11]

# the list of all compiled regex expressions
regex = map(lambda x:re.compile(x), patterns)
regex = list(regex)

# The list of answers occur in patterns dictionary
answers = list(patterns.values())

# A simple preprocessing function. 
# It removes punctuation, replaces clitics with regarding words and does case folding for normalization.
def preprocess(msg):
    if len(msg)<1:
        return msg
    msg = remove_punctuations(msg)
    if len(msg)<1:
        return msg
    msg = replace_clitics(msg)
    if len(msg)<1:
        return msg
    msg, changed_words = case_folding(msg)
    if len(msg)<1:
        return msg

    return msg, changed_words

# Removes punctutations at the end of the sentences.
def remove_punctuations(msg):
    if msg[-1] in ['.', '?', ':', ';', ',']:
        return msg[0:-1]
    return msg

# Replaces clitics with regarding words.
# Returns error message if an undefined clitic is given
def replace_clitics(msg):
    global clitic_set

    clitic = 'none'
    words = tokenizer(msg)
    msg_proc = ''
    for word in words:
        i = 0
        for char in word:
            i += 1
            if clitic != 'none':
                if(char == 's'):
                    clitic = 'none'
                    break
                clitic += char
 
            if char == '\'':
                clitic = ''
                word = word[0:i-1]

        if clitic != 'none':
            try:
                msg_proc = msg_proc + word + ' ' + clitic_set[clitic] + ' '
                clitic = 'none'
            except:
                print(colored("> I think you've misspelled something.", 'green'))
                return msg
        else:
            msg_proc = msg_proc + word + ' '

    return msg_proc[0:-1]

# Splits a text by spaces
# Tokens can be thought as words.
def tokenizer(str):
    str += ' '
    words = []
    word = ''
    for char in str:
        if char == ' ':
            words.append(word)
            word = ''      
        else:
            word += char
    
    return words

# Turns a given text into lowercase
def case_folding(msg):
    global char_set

    words = tokenizer(msg)
    changed_words = {}
    msg_lower = ''

    for word in words:
        if re.search('.*[A-Z].*', word):
            word_lower = ''
            for char in word:
                if char in char_set.keys():
                    char = char_set[char]
                word_lower += char
            changed_words[word] = word_lower
            word = word_lower
        msg_lower = msg_lower + word + ' '
    
    msg_lower = msg_lower[0:-1]
    return msg_lower, changed_words

###################################################################################
###################################################################################
############################## MAIN LOOP ##########################################
###################################################################################
###################################################################################

print(colored(WELCOME_MSG, 'green'))

seq_started = False #Cheks whether any question that starts a sequence is asked
seq_prefix = '' #For the detection of the first answer regarding sequence 
seq_suffix = '' #For the detection of the second answer regarding sequence

while True:
    msg = input('You: ')
    msg, _ = preprocess(msg)
    if seq_started:
        msg = seq_prefix + msg + seq_suffix

    for idx, exp in enumerate(regex):
        is_responded = False
        no_match = False
        match = exp.match(msg)
        if match:
            if idx == 15: #15 is the index of sequnce quitter.
                seq_started = False
                seq_prefix = ''
                seq_suffix = ''
            elif idx in sequences: #Checks whether the question starts a sequence or not
                seq_started = True
                seq_prefix = str(idx+1) + '_'
            elif seq_prefix != '':
                seq_suffix = '_' + seq_prefix[0:-1]
                seq_prefix = ''
            else:
                seq_started = False
                seq_suffix = ''
            words_in_ans = tokenizer(answers[idx])
            ans = '> '
            for word in words_in_ans:
                if word == '#':
                    try:
                        word = meanings[match.group(1)]
                    except:
                        if idx<2:
                            print(colored(NO_MATCH_ANSWER, 'green'))
                            no_match = True
                            is_responded = True
                        word = match.group(1)
                ans = ans + word + ' '
            if not no_match:
                print(colored(ans[0:-1], 'green'))
                is_responded = True    
            break

    if not is_responded:  
        if seq_started:
            print(colored(NOT_UNDERSTOOD_ANSWER, 'green'))
        else:
            print(colored(DEFAULT_RESPONSE, 'green'))
