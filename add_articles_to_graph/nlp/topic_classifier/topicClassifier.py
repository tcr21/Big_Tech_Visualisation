"""
File:           topic.py
Author:         Ted Jenks
Creation Date:  23/01/2022
Last Edit Date: 23/01/2022
Last Edit By:   Ted Jenks

Functions:      topic(text)

Summary of File:

        Contains functions to run topic analysis on a piece of text using
        a vote based classifier developed using Spacy.
        NOT IN USE.
"""

from add_articles_to_graph.nlp.topic_classifier.setup.tokenizer import tokenizer
import os
import sys
import pickle
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

# -------------------------------------------------------------------------------
# ----------------------------Load Data and Model--------------------------------
# -------------------------------------------------------------------------------

# for more info on the storage protocal used here look at pickle documentation

classifier_f = open(
    "add_articles_to_graph/nlp/topic_classifier/setup/pickle/classifier.pickle",
    "rb",
)
classifiers = pickle.load(classifier_f)
classifier_f.close()

classifier = classifiers[0]


def topic(text):
    """
    Get the classification of a piece of text.

    Args:
        text (str): input.

    Returns:
        str: classification.
    """
    if text == "":
        return ""
    return classifier.predict([text])[0]
