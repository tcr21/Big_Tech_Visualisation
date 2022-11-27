import numpy as np


class Preprocessor:
    def __init__(self, text) -> None:
        self.backslash_chars = {"\a", "\b", "\e", " \f", "\n", "\r", "\t", "\t", "\v"}
        self._original_text = text
        self._text = text

    def revert(self):
        self._text = self._original_text
        return self._original_text

    def get_original(self):
        return self._original_text

    def get_text(self):
        return self._text

    def remove_esc_chars(self):
        escapes = "".join([chr(char) for char in range(1, 32)])
        translator = str.maketrans("", "", escapes)
        self._text = self._text.translate(translator)


test = "here is an \n example of \t what we need"

pp = Preprocessor(test)
pp.remove_esc_chars()
print(pp.get_text())
