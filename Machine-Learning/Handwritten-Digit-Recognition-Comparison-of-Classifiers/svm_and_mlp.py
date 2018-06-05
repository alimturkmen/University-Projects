#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 20 14:54:22 2018

@author: furkan
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, metrics
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

import itertools

f = np.load("data/mnist.npz")
x_train, y_train = f['x_train'], f['y_train']
x_test, y_test = f['x_test'], f['y_test']
f.close()

num_classes = 10


x_train=x_train.reshape(60000, 784)
x_test=x_test.reshape(10000, 784)


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.min() + (cm.max()-cm.min()) / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()




## Train SVM Classifier
classifier = svm.LinearSVC()
classifier.fit(x_train, y_train)

## Run the classifier on test data
pred = classifier.predict(x_test)

confusion_mtx = confusion_matrix(y_test, pred)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))

## Classifier report
print ("SVM Classifier Report")
print (metrics.classification_report(y_test, pred))
print ('Test accuracy:', metrics.accuracy_score(y_test, pred))

## Train MLP Classifier
classifier = MLPClassifier()
classifier.fit(x_train, y_train)

## Run the classifier on test data
pred = classifier.predict(x_test)

confusion_mtx = confusion_matrix(y_test, pred)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))

## Classifier report
print ("MLP Classifier Report")
print (metrics.classification_report(y_test, pred))
print ('Test accuracy:', metrics.accuracy_score(y_test, pred))




