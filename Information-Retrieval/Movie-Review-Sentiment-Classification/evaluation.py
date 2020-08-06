class Evaluate(object):

    def __init__(self, predictions, labels, num_of_cls):
        self.predictions = predictions # Model predictions
        self.labels = labels # True labels
        self.num_of_cls = num_of_cls # Number of classes in the dataset
        self.confusion_matrix = self.create_confusion_matrix()
      
    # Creates confusion matrix of the model's results. 
    def create_confusion_matrix(self):
        number_of_classes = self.num_of_cls
        predictions = self.predictions
        y = self.labels

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
    def calc_macro_metrics(self):
        confusion_matrix = self.confusion_matrix
        number_of_classes = self.num_of_cls
        predictions = self.predictions
        y = self.labels

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

        precision = precision/number_of_classes
        recall = recall/number_of_classes
        macro_metrics['precision'] = precision
        macro_metrics['recall'] = recall
        if  precision+recall != 0:
            macro_metrics['f1'] = 2*recall*precision/(precision+recall)
        else:
            macro_metrics['f1'] = 0

        return macro_metrics

    # Calculates micro-average precision, recall and f1 scores.
    def calc_micro_metrics(self):
        confusion_matrix = self.confusion_matrix
        number_of_classes = self.num_of_cls
        predictions = self.predictions
        y = self.labels

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



        
