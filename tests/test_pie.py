import sys
import os
import json
import shutil

import bupytest

sys.path.insert(0, './')
from pie import pie


class TestPie(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.pie = pie.Pie()
        
        if os.path.isdir('tests/pie-test'):
            shutil.rmtree('tests/pie-test')

        os.mkdir('tests/pie-test')

        with open('tests/pie-test/01.txt', 'w') as writer:
            writer.write('Hello world!')

        with open('tests/pie-test/02.txt', 'w') as writer:
            writer.write('Good morning.')

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

        # temporary removal
        shutil.rmtree('.pie')


if __name__ == '__main__':
    bupytest.this()
