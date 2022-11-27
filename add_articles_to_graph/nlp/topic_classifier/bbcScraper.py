"""
File:           bbcScraper.py
Author:         Ted Jenks
Creation Date:  23/01/2022
Last Edit Date: 23/01/2022
Last Edit By:   Ted Jenks

Summary of File:

        Simple script to get the current top stories from BBC news.
        NOT IN USE.
"""

import requests

url = (
    "http://newsapi.org/v2/top-headlines?"
    "sources=bbc-news&"
    "apiKey=39a45ceab9df4e0d92b648ff8b747ce4"
)
response = requests.get(url)
response_dict = response.json()


def get_top_stories():
    """
    function to get top stories from BBC and return text for topic
    classification.

    Returns:
        arr<str>: texts for classification.
        arr<str>: headlines of articles.
    """
    for x in response_dict:
        """
        Move through dict of stories.
        """
        if x == "articles":
            """
            Save articles.
            """
            response_list = response_dict[x]
    texts = []
    headlines = []
    for i in response_list:
        """
        Generate text for NLP from list.
        """
        headlines.append(i["title"])
        text = i["title"] + " " + i["description"]
        texts.append(text)
    return texts, headlines
