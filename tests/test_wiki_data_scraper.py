from urllib import response
import pytest
import unittest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# from visualisation_app/app.py import app object
from graph_db_generator.wiki_data_retriever import WikiDataRetriever


class TestWikiDataScraper(unittest.TestCase):
    def test_get_name_gets_correct_name(self):
        company = WikiDataRetriever("Q380")
        company_name = company.get_name()
        self.assertEqual(company_name.lower(), "meta platforms")

    def test_get_description_gets_correct_description(self):
        company = WikiDataRetriever("Q380")
        company_description = company.get_description()
        self.assertEqual(
            company_description.lower(), "american social media and technology company"
        )

    def test_get_property_values_gives_correct_entities(self):
        correct = [
            "Q16321326",
            "Q29123981",
            "Q52410688",
            "Q61058375",
            "Q19865830",
            "Q64732680",
            "Q92586587",
            "Q81063275",
            "Q17985544",
            "Q85760291",
            "Q106859693",
            "Q209330",
            "Q28943651",
        ]
        company = WikiDataRetriever("Q380")
        (
            names,
            entity_codes,
            descriptions,
            humans,
            locations,
        ) = company.get_property_values("P355")
        for retrieved, correct in zip(entity_codes, correct):
            self.assertEqual(retrieved, correct)
