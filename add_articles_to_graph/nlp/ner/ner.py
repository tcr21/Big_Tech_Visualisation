"""
File:           ner.py
Author:         Ben Kirwan
Creation Date:  03/02/2022
Last Edit Date: 05/03/2022
Last Edit By:   Ben Kirwan

Functions:      entities(raw)

Summary of File:

    Contains entities function which uses our fine-tuned BERT model for NER
"""

import torch
import numpy as np
from transformers import BertTokenizer
import os


tag_values = [
    "I-geo",
    "2",
    "B-per",
    "B-tim",
    "5",
    "I-per",
    "O",
    "8",
    "I-org",
    "10",
    "B-gpe",
    "I-tim",
    "B-geo",
    "14",
    "15",
    "16",
    "B-org",
    "PAD",
]

tokenizer = BertTokenizer.from_pretrained("bert-base-cased", do_lower_case=False)

fn = os.path.join(os.path.dirname(__file__), "NER_model1")
model = torch.load(fn)


def entities(raw):
    """
    Function takes in strings of text and returns tuple containing
    lists of people, organisations, and gpes
    Args:
        raw (str): input.

    Returns:
        tuple(<array>string,<array>string,<array>string)
    """
    persons = []
    orgs = []
    gpes = []
    tokenized_sentence = tokenizer.encode(raw)
    input_ids = torch.tensor([tokenized_sentence])

    with torch.no_grad():
        output = model(input_ids)

    label_indices = np.argmax(output[0].to("cpu").numpy(), axis=2)

    tokens = tokenizer.convert_ids_to_tokens(input_ids.to("cpu").numpy()[0])
    new_tokens, new_labels = [], []
    for token, label_idx in zip(tokens, label_indices[0]):
        if token.startswith("##"):
            new_tokens[-1] = new_tokens[-1] + token[2:]
        else:
            new_labels.append(tag_values[label_idx])
            new_tokens.append(token)

    for token, label in zip(new_tokens, new_labels):
        if label == "B-per":
            persons.append(token)
        if label == "B-org":
            orgs.append(token)
        if label == "B-geo" or label == "B-gpe":
            gpes.append(token)

        if label == "I-per" and persons != []:
            persons[-1] = persons[-1] + " " + token
        if label == "I-org" and orgs != []:
            orgs[-1] = orgs[-1] + " " + token
        if (label == "I-geo" or label == "I-gepe") and gpes != []:
            gpes[-1] = gpes[-1] + " " + token

    persons = list(set(persons))
    orgs = list(set(orgs))
    gpes = list(set(gpes))
    return persons, orgs, gpes


########  TESTING THE BERT NER MODEL    #############

# import os
# from pymongo import MongoClient
# import pymongo
# import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# mongoDB = 'mongodb+srv://nathanflegg:fmpuRJWRe7p7xRL@cluster0.w1pgf.mongodb.net/visualising_news'
# # print(os.getenv('MONGODB_SERVER'))
# client = MongoClient(mongoDB)
# db = client.visualising_news

# recent = list(db.raw_articles.find(
# sort=[('_id', pymongo.DESCENDING)]).limit(10))
# for article in recent:
#     print(article["title"][0] + "\n" + str(entities(article["title"][0]))+"\n\n")


############ OLD NER MODEL #################


# import spacy
# nlp = spacy.load('en_core_web_sm')


# def entities(raw):
#     """
#     Function takes in strings of text and returns tuple containing
#     lists of people, organisations, and gpes
#     Args:
#         raw (str): input.

#     Returns:
#         tuple(<array>string,<array>string,<array>string)
#     """
#     processed = nlp(raw)
#     persons = []
#     orgs = []
#     gpes = []
#     for ent in processed.ents:
#         label = ent.label_
#         text = ent.text
#         if (label == "PERSON"):
#             persons.append(text)
#         if (label == "ORG"):
#             orgs.append(text)
#         if(label == "GPE"):
#             gpes.append(text)
#     persons = list(set(persons))
#     orgs = list(set(orgs))
#     gpes = list(set(gpes))
#     return persons, orgs, gpes
