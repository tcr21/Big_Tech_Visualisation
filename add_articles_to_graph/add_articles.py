"""
File:           add_articles.py
Author:         Ted Jenks
Creation Date:  03/02/2022
Last Edit Date: 16/05/2022
Last Edit By:   Ted Jenks

Functions:      update_graph(), add_article(article_data),
                match_and_link(story, entities, label, prop='name')

Summary of File:

    Contains functions to add stories to graph DB using NLP
"""

from dotenv import load_dotenv
from py2neo.matching import *
from py2neo import Graph, Node, Relationship
import pymongo
from pymongo import MongoClient
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from add_articles_to_graph.date_time_converter import get_datetime
from add_articles_to_graph.nlp.ner.srl import link_finder
from add_articles_to_graph.trending_indices import update_trending_indices
from add_articles_to_graph.neo4j_article_linker import article_linker

load_dotenv()

# Bring in .env variables
mongoDB = os.getenv("MONGODB_SERVER")
neo4j_uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

client = MongoClient(mongoDB)
db = client.visualising_news

g = Graph(neo4j_uri, auth=(username, password))
nodes = NodeMatcher(g)


def update_graph():
    """
    Update the graphDB with data from the articles DB.
    Uses the 10 most recent entries.
    """
    recent = list(db.raw_articles.find(sort=[("_id", pymongo.DESCENDING)]).limit(100))
    for article in recent:
        add_article(article)


def match_and_link(story, entities, label, prop="name"):
    """
    Find matching entities in the graph and link stories to them.
    The function's many try/catches account for different text formats from
    articles.

    Args:
        story (dict): Story data.
        entities (list): list of enitities in story.
        label (str): Type of nodes to look for.
        prop (str, optional): Property to compare. Defaults to 'name'.
    """
    for entity in entities:
        # filter stop words and catagories from headlines
        if (entity.lower() == "guardian" 
            or entity.lower() == 'zdnet' 
            or entity.lower() == 'bbc news'
            or entity.lower() == 'the'
            or entity.lower() == 'a'
            or entity.lower() == 'global'
            or entity.lower() == 'un'
            or entity.lower() == 'music'
            or entity.lower() == 'street'
            or entity.lower() == 'group'
            or entity.lower() == 'street'
            or len(entity) < 4):
            continue
        try:
            # try to match exact nodes which are industry giants
            matching_nodes = nodes.match(label).where(
                'toLower(_.name) = toLower("%s")' % entity, _industry_giant=True
            )
            if matching_nodes.exists():
                link_story_to_entity(label, matching_nodes, prop, story)
                continue
            # try to match similar nodes which are industry giants
            matching_nodes = nodes.match(label).where(
                'toLower(_.name) CONTAINS toLower("%s")' % entity, _industry_giant=True
            )
            if matching_nodes.exists():
                link_story_to_entity(label, matching_nodes, prop, story)
                continue
            # try to match exact nodes which aren't industry giants
            matching_nodes = nodes.match(label).where(
                'toLower(_.name) = toLower("%s")' % entity
            )
            if matching_nodes.exists():
                link_story_to_entity(label, matching_nodes, prop, story)
                continue
            # try to match similar nodes which are industry giants
            matching_nodes = nodes.match(label).where(
                'toLower(_.name) CONTAINS toLower("%s")' % (entity + " "),
                _industry_giant=True,
            )
            if matching_nodes.exists():
                link_story_to_entity(label, matching_nodes, prop, story)
                continue
            # try to match similar nodes which aren't industry giants
            matching_nodes = nodes.match(label).where(
                'toLower(_.name) CONTAINS toLower("%s")' % (entity + " ")
            )
            if matching_nodes.exists():
                link_story_to_entity(label, matching_nodes, prop, story)
        except:
            # do nothing
            pass


def link_story_to_entity(label, matching_nodes, prop, story):
    for node in matching_nodes:
        link = Relationship(node, prop.capitalize(), story)
        g.merge(link, label, '_uid')


def add_article(article_data):
    """
    Add an article to the graph DB

    Args:
        article_data (dict): Story data.
    """
    print("Adding article:", article_data["title"][0])
    raw_date = article_data["date"][0]
    if type(raw_date) == type(None):
        print("Reject\n")
        return
    datetime_object = get_datetime(raw_date)
    people, organisations, locations, link = link_finder(
        article_data['title'][0])
    story = Node('News', _uid=str(article_data['_id']),
                 name=article_data['title'][0],
                 date=datetime_object.strftime("%x"),
                 _people=" ".join([person.lower() for person in people]),
                 _organisations=" ".join([organisation.lower()
                                          for organisation in organisations]) + ' ',
                 _locations=" ".join([location.lower()
                                      for location in locations]) + ' ')
    g.merge(story,'News', '_uid')
    # article_linker(story, str(article_data['_id']), people, '_people')
    # article_linker(story, str(
    #     article_data['_id']), organisations, '_organisations')
    # article_linker(story, str(article_data['_id']), locations, '_locations')
    if link is not None:
        match_and_link(story, people, 'Person', link)
        match_and_link(story, organisations, 'Parent', link)
        match_and_link(story, organisations, 'Subsidiary', link)
        match_and_link(story, organisations, 'Shareholder', link)
    else:
        match_and_link(story, people, 'Person')
        match_and_link(story, organisations, 'Parent')
        match_and_link(story, organisations, 'Subsidiary')
        match_and_link(story, organisations, 'Shareholder')
    match_and_link(story, locations, 'Parent', 'location')
    print('Done\n')


if __name__ == "__main__":
    update_graph()
    update_trending_indices()
