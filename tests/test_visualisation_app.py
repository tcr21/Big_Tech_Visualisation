from urllib import response
import pytest
import unittest
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# from visualisation_app/app.py import app object
from visualisation_app.app import app


class TestVisualisationApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_other(self):
        tester = app.test_client(self)
        response = tester.get("a", content_type="html/text")
        self.assertEqual(response.status_code, 404)

    def test_api(self):
        tester = app.test_client(self)
        response = tester.get("/api", content_type="html/text")
        self.assertEqual(response.status_code, 200)

        keys = ["links", "source", "target", "label"]
        for key in keys:
            self.assertTrue(key.encode() in response.data)
