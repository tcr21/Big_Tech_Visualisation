import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from add_articles_to_graph.nlp.ner.ner import entities

def test_classifier_returns_tuple():
    assert isinstance(entities("test"), tuple)

def test_returns_three_empty_lists_on_empty_input():
    assert entities("") == ([],[],[])

def test_entity_recognition():
    assert entities("Meta announced their intention to lay off staff") == ([],["Meta"],[])
