import sys
import os
import json

import bupytest

sys.path.insert(0, './')
from pie import pie


class TestPie(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.pie = pie.Pie()

    def test_create_repository(self):
        author = 'Jaedson'
        author_email = 'imunknowuser@protonmail.com'

        self.pie.create_repository(author, author_email)

        self.assert_true(os.path.isdir('.pie'))
        self.assert_true(os.path.isfile('.pie/.info'))

        with open('./.pie/.info', 'r') as reader:
            repository_info = json.load(reader)

        self.assert_expected(repository_info['author'], author)
        self.assert_expected(repository_info['author_email'], author_email)
        self.assert_expected(len(repository_info['key']), 64)
        self.assert_expected(repository_info['remote'], None)


if __name__ == '__main__':
    bupytest.this()
