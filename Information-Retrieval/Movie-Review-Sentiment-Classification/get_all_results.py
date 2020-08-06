from model import NaiveBayes
from preprocess import Preprocess 

neg_path = 'data\\data\\train\\neg\\'
pos_path = 'data\\data\\train\\pos\\'
test_path_pos = 'data\\data\\test\\pos\\'
test_path_neg = 'data\\data\\test\\neg\\'
p = Preprocess()

# Takes smoothing(use or not), stop_words(remove or not) and model name(Multinomial, Bernoulli or Binary) as parameters
# Reads the files in a given directory path.
# Processes documents in the directory and tokenize them.
# Using this tokenized documents, trains Naive Bayes model.
# After training tests the model with the documents in the given test directory.
# Gets the score of the model.
# Writes score of the model under scores directory,
#        predictions of the model under predictions directory,
#        and the model itself under models directory.
# Returns labels, predictions of the model and the model.
def get_results(stop_words, model_name, smoothing):

    train_neg, count_neg, train_labels_neg = p.read_norm_multifile(neg_path, remove_stop_words=stop_words)
    train_pos, count_pos, train_labels_pos = p.read_norm_multifile(pos_path, remove_stop_words=stop_words)
    train_data = train_neg + train_pos
    train_label = train_labels_neg + train_labels_pos
    doc_counts = {0:count_neg, 1:count_pos}
    test_neg, _, labels_neg = p.read_norm_multifile(test_path_neg, remove_stop_words=stop_words)
    test_pos, _, labels_pos = p.read_norm_multifile(test_path_pos, remove_stop_words=stop_words)
    test_set = test_neg + test_pos
    labels = labels_neg + labels_pos

    model = NaiveBayes(model_name)
    model.train(train_data, train_label, doc_counts, smoothing=smoothing)
    model.save_model(file_name=('models\\'+model_name+str(smoothing)))
    preds, metrics = model.test(test_set, labels)

    f = open('scores\\stats_'+model_name+'_'+str(smoothing), 'w')
    for m in metrics.keys():
        f.write(m+'-averaged scores\n')
        for metric in metrics[m].keys():
            f.write(metric+':'+str(metrics[m][metric])+'\n')
        f.write('\n')

    f = open('predictions\\preds_'+model_name+'_'+str(smoothing), 'w')
    f.write('T\tP\n')
    for idx, label in enumerate(labels):
        f.write(str(label))
        f.write('\t')
        f.write(str(preds[idx]))
        f.write('\n')

    return labels, preds, model

get_results(False, 'Binary', True)
_, preds_bin, _, = get_results(False, 'Binary', False)
get_results(False, 'Multinomial', True)
_, preds_mnb, _, = get_results(False, 'Multinomial', False)
get_results(False, 'Bernoulli', True)
labels, preds_bnb, model = get_results(False, 'Bernoulli', False)


print('Binary-Multinomial:')
print(model.randomization_test(labels, preds_bin, preds_mnb))
print('***')
print('Binary-Bernoulli:')
print(model.randomization_test(labels, preds_bin, preds_bnb))
print('***')
print('Multinomial-Bernoulli:')
print(model.randomization_test(labels, preds_mnb, preds_bnb))


