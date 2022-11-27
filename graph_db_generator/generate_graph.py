"""
File:           generate_graph.py
Author:         Ted Jenks
Creation Date:  03/02/2022
Last Edit Date: 05/03/2022
Last Edit By:   Ted Jenks

Functions:      generate_graph(company_code)

Summary of File:

    Contains the function to build a neo4j graph from wikidata content.
"""

from dotenv import load_dotenv
import pickle
from py2neo import Graph, Node, Relationship

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from graph_db_generator.wiki_data_retriever import WikiDataRetriever

load_dotenv()

# Bring in .env variables
neo4j_uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

# connect to server
g = Graph(neo4j_uri, auth=(username, password))

# the properties of the companies we look into:
properties = {
    "subsidiaries": "P355",
    "board_members": "P3320",
    "owners": "P127",
    "founders": "P112",
}

# the companies that wikiData is scraped for:
big_companies = {
    "meta": "Q380",
    "alphabet": "Q20800404",
    "google": "Q95",
    "amazon": "Q3884",
    "microsoft": "Q2283",
    "netflix": "Q907311",
    "tencent": "Q860580",
    "nvidea": "Q182477",
    "tesla": "Q478214",
    "cisco": "Q173395",
    "oracle": "Q19900",
    "amd": "Q128896",
    "sony": "Q41187",
    "apple": "Q312",
    "twitter": "Q918",
}

entities = {
    "meta": "Parent",
    "alphabet": "Parent",
    "google": "Parent",
    "amazon": "Parent",
    "microsoft": "Parent",
    "netflix": "Parent",
    "tencent": "Parent",
    "nvidea": "Parent",
    "tesla": "Parent",
    "cisco": "Parent",
    "oracle": "Parent",
    "amd": "Parent",
    "sony": "Parent",
    "apple": "Parent",
    "twitter": "Parent",
}


def generate_graph(company_code):
    """
    Generate a neo4j graph database based on information scraped from wikidata.

    Args:
        company_code (str): 'Q-code' of the starting company of the study.
    """
    company = WikiDataRetriever(company_code)
    company_name = company.get_name()
    company_description = company.get_description()
    company_location = company.get_location()
    head = Node(
        "Parent",
        _uid=company_code.lower(),
        name=company_name,
        description=company_description,
        _industry_giant=True,
        _location=company_location,
        heat=0,
    )
    g.merge(head, "Parent", "_uid")
    for key in properties:
        (names,
         entity_codes,
         descriptions,
         humans,
         locations) = company.get_property_values(properties[key])
        for name, code, description, human, location in zip(names,
                                                            entity_codes,
                                                            descriptions,
                                                            humans,
                                                            locations):
            # ignore regional subsidiaries
            if ((company_name.lower() in name.lower() 
                or 'facebook' in name.lower()
                or 'apple' in name.lower()
                or 'amazon' in name.lower()
                or 'tesla' in name.lower()
                or 'google' in name.lower())
                # special condition for facebook as it has regionals but not parent
                and name.lower() != 'facebook technologies, llc'):
                continue
            if human:
                label = 'Person'
                entities[name.lower()] = 'Person'
            elif key == 'owners':
                label = 'Shareholder'
                entities[name.lower()] = 'Shareholder'
            else:
                label = 'Subsidiary'
                entities[name.lower()] = 'Subsidiary'
            entity = Node(label, _uid=code, name=name,
                          description=description, _location=location,
                          heat=0)
            link = Relationship(head, key.capitalize(), entity)
            g.merge(link, label, '_uid')


if __name__ == "__main__":
    for key in big_companies:
        generate_graph(big_companies[key])

    # save entities in known vocab
    with open("graph_db_generator/entities.pickle", "wb") as target:
        pickle.dump(entities, target)
