import pytest

from .context import pystats


class TestCode:

    def setup_method(self, test_method):
        path = 'tests/data/sample.py'
        with open(path, 'rb') as f:
            code = f.read()
            self.code = pystats.Code(path, code)

    def test_count_lines(self):
        assert self.code.count_lines() == 14
    
    def test_count_blank_lines(self):
        assert self.code.count_blank_lines() == 4

    def test_count_inline_comments(self):
        assert self.code.count_inline_comments() == 1

    def test_count_block_comments(self):
        assert self.code.count_block_comments() == 4

    def test_count_approximate_function_length(self):
        count, length = self.code.count_approximate_function_length()
        assert count == 2
        assert length == 3

    def test_get_languages(self):
        assert self.code.get_languages() == ['Python']
