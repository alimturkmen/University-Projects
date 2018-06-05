# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:46:41 2018

@author: Deniz
"""

%matplotlib inline
import keras
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools

f = np.load("data/mnist.npz")
x_train, y_train = f['x_train'], f['y_train']
x_test, y_test = f['x_test'], f['y_test']
f.close()

img_rows, img_cols = x_train.shape[1:3]
batch_size = 100
num_classes = 10
epochs = 1

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

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


# TRIVIAL BASELINE MODEL
class BaselineModel:
    def __init__(self, num_of_classes):
        self.num_of_classes = num_of_classes
    
    def predict_classes(self, inputs):
        return np.random.randint(0, self.num_of_classes, len(inputs))

baseline_model = BaselineModel(num_classes)
pred_labels = baseline_model.predict_classes(x_test)
real_labels = np.argmax(y_test, axis=1)
label_err = pred_labels - real_labels
idx = np.where(label_err!=0)[0]
print('Test accuracy:', (1-len(idx)/len(label_err)))
confusion_mtx = confusion_matrix(real_labels, pred_labels)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))


# BUILD CNN MODEL
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

cnn_model = Sequential()
cnn_model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape,
                     kernel_initializer=keras.initializers.VarianceScaling()))
cnn_model.add(Conv2D(64, (3, 3), activation='relu',
                     kernel_initializer=keras.initializers.VarianceScaling()))
cnn_model.add(MaxPooling2D(pool_size=(2, 2)))
cnn_model.add(Dropout(0.25))
cnn_model.add(Flatten())
cnn_model.add(Dense(128, activation='relu',
                    kernel_initializer=keras.initializers.VarianceScaling()))
cnn_model.add(Dropout(0.5))
cnn_model.add(Dense(num_classes, activation='softmax',
                    kernel_initializer=keras.initializers.VarianceScaling()))

cnn_model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.RMSprop(),
                  metrics=['accuracy'])

cnn_model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(x_test, y_test))
# cnn_model.save('MODELS/CNN_model.h5')
# from keras.models import load_model
# cnn_model = load_model('MODELS/CNN_model.h5')

pred = cnn_model.predict(x_test)
pred_labels = np.argmax(pred, axis=1)
real_labels = np.argmax(y_test, axis=1)
label_err = pred_labels - real_labels
idx = np.where(label_err!=0)[0]
worst_err = np.abs(pred-y_test)[idx, real_labels[idx].astype(int)]
worst_idx = np.flip(np.argsort(worst_err), axis=0)

print('Test accuracy:', (1-len(idx)/len(label_err)))
confusion_mtx = confusion_matrix(real_labels, pred_labels)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))

# A few of the wrong predicted digits
for i in range(min(9, len(worst_err))):
    plt.subplot(3,3,i+1)
    plt.imshow(x_test[idx[worst_idx[i]]].reshape(img_rows, img_cols), cmap='gray', interpolation='none')
    plt.title("class {}, pred {}".format(real_labels[idx[worst_idx[i]]], pred_labels[idx[worst_idx[i]]]))
plt.tight_layout()


# BUILD K Nearest Neighbour MODEL
from sklearn.neighbors import KNeighborsClassifier

knn_model = KNeighborsClassifier(n_neighbors=10, weights='uniform', p=3, n_jobs=-1)
real_labels = np.argmax(y_train, axis=1)
knn_model.fit(x_train.reshape(x_train.shape[0], img_rows*img_cols), real_labels)
# from sklearn.externals import joblib
# joblib.dump(knn_model, "MODELS/knn_model.dump", compress=3)
# knn_model = joblib.load("MODELS/knn_model.dump")

pred_labels = knn_model.predict(x_test.reshape(x_test.shape[0], img_rows*img_cols))
# pred_labels.dump("MODELS/knn_predicted_labels.txt")
# pred_labels = np.load("MODELS/knn_predicted_labels.txt")
real_labels = np.argmax(y_test, axis=1)
label_err = pred_labels - real_labels
idx = np.where(label_err!=0)[0]
print('Test accuracy:', (1-len(idx)/len(label_err)))
confusion_mtx = confusion_matrix(real_labels, pred_labels)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))


# BUILD SVM MODEL
from sklearn import svm, metrics

classifier = svm.LinearSVC()
classifier.fit(x_train, y_train)
## Run the classifier on test data
pred = classifier.predict(x_test)

print ('Test accuracy:', metrics.accuracy_score(y_test, pred))
confusion_mtx = confusion_matrix(y_test, pred)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))


# BUILD MLP CLASSIFIER MODEL
from sklearn.neural_network import MLPClassifier

classifier = MLPClassifier()
classifier.fit(x_train, y_train)

## Run the classifier on test data
pred = classifier.predict(x_test)

print ('Test accuracy:', metrics.accuracy_score(y_test, pred))
confusion_mtx = confusion_matrix(y_test, pred)
plot_confusion_matrix(confusion_mtx, classes = range(num_classes))
