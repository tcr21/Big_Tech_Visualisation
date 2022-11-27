"""
File:           init.py
Author:         Tiphaine Ramenason, Ted Jenks
Creation Date:  21/01/2022
Last Edit Date: 23/01/2022
Last Edit By:   Ted Jenks

Functions:      train_classifier(classifier, tokenizer, data)

Summary of File:

        Contains functions to train a simple spacy classifier.
"""

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../.."))
from add_articles_to_graph.nlp.topic_classifier.setup.tokenizer import tokenizer

#%%

data = pd.read_json(
    "add_articles_to_graph/nlp/topic_classifier/setup/data/News_Category_Dataset_v2.json",
    lines=True,
)
# read data from file.
data["text"] = data.headline + " " + data.short_description
# combine headline and description into one string.
categories = data.groupby("category")
# record the categories.


def train_classifier(classifier, tokenizer, data):
    """
    Function to train a classifier.

    Args:
        classifier (classifier): the classifier to be used in the analyser.
        tokenizer (func): the function to be used for tokenizing the data.
        data (dict): the data for training

    Returns:
        classifier: a trained classifier.
    """
    tfidata = TfidfVectorizer(tokenizer=tokenizer)
    # define features with tf-idf.
    X = data["text"]
    Y = data["category"]
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.1, random_state=42
    )
    # choose training and testing data at random.
    clf = Pipeline([("tfidata", tfidata), ("clf", classifier)])
    # setup classifier with the features and model.
    clf.fit(X_train, Y_train)
    # train the model.
    Y_pred = clf.predict(X_test)
    # generate tet data predictions.
    print(classification_report(Y_test, Y_pred))
    print(confusion_matrix(Y_test, Y_pred))
    # print training metrics.
    return clf


#%%
classifiers = [LinearSVC()]  # , MLPClassifier(verbose=True)
clf = []
for c in classifiers:
    clf.append(train_classifier(c, tokenizer, data))

save_classifiers = open(
    "add_articles_to_graph/nlp/topic_classifier/setup/pickle/classifier.pickle",
    "wb",
)
pickle.dump(clf, save_classifiers)
save_classifiers.close()
