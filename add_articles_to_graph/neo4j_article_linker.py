"""
File:           neo4j_article_linker.py
Author:         Ted Jenks
Creation Date:  14/05/2022
Last Edit Date: 14/05/2022
Last Edit By:   Ted Jenks

Functions:      article_linker(story, story_uid, entities, prop)

Summary of File:

    Contains functions to link an article to entities.
"""

from py2neo import Graph, Node, Relationship
from py2neo.matching import *
import os

neo4j_uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

g = Graph(neo4j_uri, auth=(username, password))
nodes = NodeMatcher(g)


def article_linker(story, story_uid, entities, prop="people"):
    """
    Add links between articles.

    Args:
        story (Node): The story of node
        story_uid (str): uid of story
        entities (list<str>): List of entitiies
        prop (str, optional): Property to link by. Defaults to 'people'.
    """
    for entity in entities:
        if (
            entity.lower() != "guardian"
            and entity.lower() != "zdnet"
            and entity.lower() != "bbc news"
        ):
            matching_nodes = nodes.match("Story").where(
                'toLower(_.%s) CONTAINS toLower("%s")' % (prop.lower(), entity + " "),
                _uid=NE(story_uid),
            )
            for node in matching_nodes:
                link = Relationship(node, prop.upper(), story)
                g.merge(link, "Story", "_uid")
