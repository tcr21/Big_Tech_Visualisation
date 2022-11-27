"""
File:           add_articles.py
Author:         Ben Kirwan
Creation Date:  25/02/2022
Last Edit Date: 25/02/2022
Last Edit By:   Ben Kirwan

Functions:      detect_acquisition(headlines)

Summary of File:

    Contains functions to detect relationships between entities in headlines
    NOT IN USE
"""


import spacy
import os
from pymongo import MongoClient
import pymongo
import sys
from dotenv import load_dotenv
from newscatcherapi import NewsCatcherApiClient

load_dotenv()
nlp = spacy.load("en_core_web_sm")

verb_types = {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"}

pattern = [
    {"POS": "VERB", "OP": "?"},
    {"POS": "ADV", "OP": "*"},
    {"POS": "AUX", "OP": "*"},
    {"POS": "VERB", "OP": "+"},
]


def find_verb(headline_doc):
    """returns true if lemma 'acquire' appears in headline and number of entities with label 'ORG' is at least 2

    Args:
        headline_doc (spacy.tokens): headline tokenized using 'en_core_web_sm'

    Returns:
        boolean
    """
    verbs = []
    pattern = [{"POS": "VERB"}]
    for word in headline_doc:
        if word.tag_ in verb_types:
            verbs.append(word.lemma_)
    # if len([ent.label_ for ent in headline_doc.ents if ent.label_ == 'ORG']) < 2:
    #     return None
    return verbs


def find_subject(headline_doc):
    """Finds acquired companies in a headline

    Args:
        headline_doc (spacy.tokens): headline tokenized using 'en_core_web_sm'

    Returns:
        list : list of acquired companies if there are any, else 'none'
    """
    subject_list = []
    for token in headline_doc:
        if (token.ent_type_ == "ORG") and (token.dep_ == "dobj"):
            for noun_chunk in headline_doc.noun_chunks:
                if token in noun_chunk and noun_chunk not in subject_list:
                    subject_list.append(noun_chunk)
                # check for conjuncted companies
                elif len(list(token.rights)) > 0:
                    for tright in list(token.rights):
                        if (tright.ent_type_ == "ORG") and (tright.dep_ == "conj"):
                            for noun_chunk in headline_doc.noun_chunks:
                                if (
                                    tright in noun_chunk
                                    and noun_chunk not in subject_list
                                ):
                                    subject_list.append(noun_chunk)
    if subject_list != []:
        return subject_list


def find_actor(headline_doc):
    """Finds acquiring companies in a headline

    Args:
        headline_doc (spacy.tokens): headline tokenized using 'en_core_web_sm'

    Returns:
        list : list of acquiring companies if there are any, else 'none'
    """
    actor_list = []
    for token in headline_doc:
        if (token.ent_type_ == "ORG") and (token.dep_ in ("nsubj", "ROOT")):
            for noun_chunk in headline_doc.noun_chunks:
                if token in noun_chunk and noun_chunk not in actor_list:
                    actor_list.append(noun_chunk)
                # check for conjuncted companies
                elif len(list(token.rights)) > 0:
                    for tright in list(token.rights):
                        if (tright.ent_type_ == "ORG") and (tright.dep_ == "conj"):
                            for noun_chunk in headline_doc.noun_chunks:
                                if (
                                    tright in noun_chunk
                                    and noun_chunk not in actor_list
                                ):
                                    actor_list.append(noun_chunk)
    if actor_list != []:
        return actor_list


def detect_acquisition(headline_doc):
    """detects acquisitions in a headline

    Args:
        headline_doc (spacy.tokens): headline tokenized using 'en_core_web_sm'

    Prints acquisition status of headline in form "x acquires y"

    Returns:
        list of acquiring + acquired companies in form [[acquirer],[acquired]]
    """
    action = []
    verb = find_verb(headline_doc)
    actor = find_actor(headline_doc)
    subject = find_subject(headline_doc)
    if all(t is not None for t in [actor, subject]):
        action.append([actor])
        action.append([verb])
        action.append([subject])
        print(
            str(headline_doc) + " --> " + str(actor) + str(verb) + str(subject), "\n\n"
        )
    return action if action != [] else None


#######    USING ARTICLES FROM PRNEWSWIRE.COMA AND BUSINESSWIRE.COM TO TEST FUNCTION 'DETECT_ACQUISITION'         ############

newscatcherapi = NewsCatcherApiClient(
    x_api_key="jTq-zYXyAdfUCjKNBA4dV0qRw-HCGW4YXcp-fY_LNK8"
)

acquisition_articles = newscatcherapi.get_search(
    q="business",
    search_in="title",
    lang="en",
    from_="100 hours ago",
    sources="prnewswire.com, businesswire.com",
    page_size=100,
    page=1,
)

# print(acquisition_articles)
acquisitions = []
for article in acquisition_articles["articles"]:
    acquire = detect_acquisition(nlp(article["title"]))
    if acquire != None:
        acquisitions.append(acquire)

print(acquisitions)

####### DEMONSTRATION OF CONJUNCTED COMPANIES  ###########

# detect_acquisition(nlp("Microsoft and Mitsubishi acquire Hexagon"))


#######    ACQUISITIONS FROM MONGODB   ########

# mongoDB = os.getenv('MONGODB_SERVER')

# client = MongoClient(mongoDB)
# db = client.visualising_news
# recent = list(db.raw_articles.find(
#         sort=[('_id', pymongo.DESCENDING)]).limit(10000))
# for article in recent:
#     detect_acquisition(nlp(article['title'][0]))
