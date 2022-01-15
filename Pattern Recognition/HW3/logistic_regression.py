import numpy as np
import random


# Logistic Regression Classifier
class LogisticRegression():
    def __init__(self, feature_size):
        self.feature_size = feature_size
        self.initialize_weight()


    # Initialize weight with random numbers
    def initialize_weight(self):
        self.w = np.random.random(self.feature_size)


    def train(self, x, y, lr=5.e-2, epoch=20):
        self.x = x
        self.y = y
        
        for e in range(epoch):
            for i in range(y.shape[0]):
                rand_i = random.randint(0, y.shape[0]-1)
                x_i = x[rand_i]
                y_i = y[rand_i]
                grad = np.dot(np.dot(x_i, y_i), 1/(1+np.exp(np.dot(y_i, np.dot(self.w.T, x_i)))))
                self.w += lr*grad
            to_print = "Train Loss: {}\t Train Accuracy: {}".format(self.loss(self.x, self.y), self.evaluate(x, y))
            print(to_print, end='\r')
        print()


    def predict(self, x):
        prod = np.dot(self.w.T, x)
        return 1/(1+np.exp(-prod))


    def stochastic_loss(self, x_i, y_i):
        pred = np.dot(self.w.T, x_i)
        return np.log(1+np.exp(-np.dot(y_i, pred)))


    def loss(self, x, y):
        error = 0

        for x_i, y_i in zip(x, y):
            error+= self.stochastic_loss(x_i, y_i)

        return error/(y.shape[0])


    def evaluate(self, x, y):
        tp = 0

        for x_i, y_i in zip(x, y):
            y_ = 1 if self.predict(x_i)>0.5 else -1
            if y_i == y_ : tp+=1

        return tp / y.shape[0]


    def test(self, x, y):
        to_print = "Test Loss: {}\tTest Accuracy: {}".format(self.loss(x, y), self.evaluate(x, y))
        print(to_print)


def read_data():
    train_x = np.load('train_features.npy')
    test_x = np.load('test_features.npy')
    train_y = np.load('train_labels.npy')
    test_y = np.load('test_labels.npy')

    return train_x, train_y, test_x, test_y

train_x, train_y, test_x, test_y = read_data()
classifier = LogisticRegression(train_x.shape[1])
classifier.train(train_x, train_y)
classifier.test(test_x, test_y)
