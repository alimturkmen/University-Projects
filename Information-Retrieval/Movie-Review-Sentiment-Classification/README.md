preprocess.py
This piece of code is used to clean and normalize the data. It can either take a document or a set of documents.

evaluation.py
The models are evaluated, in other words their micro and macro averaged metrics are calculated in this component.

model.py
In this module Naive Bayes models are implemented. You can train, test and evaluate Binary, Multinomial and Bernoulli NB models. It can also be used to perform randomization test. 

get_all_results.py 
It is the script written to get all of the results at once. Therefore, the parameters inside the code should be set hardcoded. 
The modules above are imported and used in this part. There is a main function doing all of the work. It takes three parameters: model name(Multinomial, Bernoulli or Binary), smoothing(whether smoothing will be used or not), and stop_words(whether stop-words are removed or not in preprocessing step) You can change the parameters that are sent to this function. By default, the three types of NB models are trained and tested one by one with and without smoothing. Then their comparison is made via randomization test.
The predictions of the models, their scores and the models themselves are stored in predictions, scores and models directories respectively.


To run the code, your python version should be 3.7 or higher. 
Also be sure that you have models, predictions and scores directories and stop_words file(if you want to remove stop-words).

After setting the parameters manually you can run the code with:
    python get_all_results.py


Default Parameters:
Negative Train Files Path - neg_path = 'data\\data\\train\\neg\\'
Positive Train Files Path - pos_path = 'data\\data\\train\\pos\\'
Negative Test Files Path - test_path_pos = 'data\\data\\test\\pos\\'
Positive Test Files Path - test_path_neg = 'data\\data\\test\\neg\\'
Remove stop_words or not - stop_words = False



