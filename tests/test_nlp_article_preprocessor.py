import pytest

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from add_articles_to_graph.nlp.article_preprocessor.preprocessor import Preprocessor


def test_can_remove_escape_chars():
    text = "hello\n\a\b\f\n\r\t\vworld"
    preprocessor = Preprocessor(text)

    preprocessor.remove_esc_chars()

    assert preprocessor.get_text() == "helloworld" and preprocessor.get_original() == text
