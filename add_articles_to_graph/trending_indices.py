"""
File:           trending_indices.py
Author:         Ted Jenks
Creation Date:  14/05/2022
Last Edit Date: 14/05/2022
Last Edit By:   Ted Jenks

Functions:      update_trending_indices(raw_date)

Summary of File:

    Contains functions to update heat scores of nodes.
"""

from dotenv import load_dotenv
from py2neo import Graph, Node
from datetime import *
import numpy as np
import os


load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

g = Graph(neo4j_uri, auth=(username, password))


def update_trending_indices():
    """
    Update the values of the trending indices.
    """
    names = g.run(
        'MATCH(n) where n: Parent OR n: Person OR n: Subsidiary OR n: Shareholder RETURN n.name, n._uid, labels(n)').to_ndarray()
    for name in names:
        heat = 0
        count = 0
        label = str(name[2][0])
        uid = str(name[1])
        name = str(name[0])
        story_dates = g.run(
            "MATCH (n {name:\"%s\"})-[r]->(s:News) RETURN s.date" % name).to_ndarray()
        count = len(story_dates)
        current = date.today()
        for i, story_date in enumerate(story_dates):
            # print(date)
            datetime_object = datetime.strptime(story_date[0], "%m/%d/%y")
            age = (current - datetime_object.date()).total_seconds()
            heat += np.exp(-(1 / (2 * 86400)) * age)
        heat = round(heat, 3)
        if heat < 0.001:
            heat = 0
        update = Node(_uid=uid, heat=float(heat))
        g.merge(update, label, "_uid")
