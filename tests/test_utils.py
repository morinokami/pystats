import pytest

from .context import utils


class TestUtils:

    def test_is_inline_comment_returns_true_for_valid_comment(self):
        assert utils.is_inline_comment(b'  # this is a comment')

    def test_is_inline_comment_returns_false_for_statement(self):
        assert not utils.is_inline_comment(b'x = 123')

    def test_extract_block_comments_returns_list_of_comments(self):
        code = b'''
"""hello world"""

def f(x):
    """doc string

    >>> f(1)
    2
    """
    return x * 2
        '''
        comments = utils.extract_block_comments(code)
        assert len(comments) == 2
        assert comments[0] == b'hello world'
        assert comments[1] == b'doc string\n\n    >>> f(1)\n    2\n    '

    def test_extract_functions_returns_function_definitions(self):
        code = '''
def f(x):
    pass

print(1)

# comment
def g(x):
    # comment
    x += 1
    return x'''
        functions = utils.extract_functions(code)
        assert len(functions) == 2
