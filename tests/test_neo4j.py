from datetime import date, datetime
import unittest
import pytest
from dotenv import load_dotenv
import sys
import os
from neo4j import GraphDatabase

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

load_dotenv()
uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(username, password))

def test_can_get_data_from_neo4j_database():
    db = driver.session()
    results = db.run("MATCH (n) RETURN n LIMIT 1")
    driver.close()
    assert results is not None
