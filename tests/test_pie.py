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

        if os.path.isdir('.pie'):
            shutil.rmtree('.pie')

        os.mkdir('tests/pie-test')

        with open('tests/pie-test/01.txt', 'w') as writer:
            writer.write('Hello world!')

        with open('tests/pie-test/02.txt', 'w') as writer:
            writer.write('Good morning.\n\nHow are you?')

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

    def test_track_file(self):
        self.pie.track_file('tests/pie-test/01.txt')
        self.pie.track_file('tests/pie-test/02.txt')

        tracked_files = self.pie.get_tracked_files()

        self.assert_expected(
            value=tracked_files['tests/pie-test/01.txt'],
            expected={
                'filename': 'tests/pie-test/01.txt',
                'commits': []
            }
        )

        self.assert_expected(
            value=tracked_files['tests/pie-test/02.txt'],
            expected={
                'filename': 'tests/pie-test/02.txt',
                'commits': []
            }
        )

    def test_index_file_lines(self):
        file_lines_1 = self.pie.index_file_lines('tests/pie-test/01.txt')
        file_lines_2 = self.pie.index_file_lines('tests/pie-test/02.txt')

        self.assert_expected(
            value=file_lines_1,
            expected={0: 'Hello world!'}
        )

        self.assert_expected(
            value=file_lines_2,
            expected={
                0: 'Good morning.',
                1: '',
                2: 'How are you?'
            }
        )

    def test_get_lines_difference(self):
        file_lines_1 = self.pie.index_file_lines('tests/pie-test/01.txt')
        file_lines_2 = self.pie.index_file_lines('tests/pie-test/02.txt')

        file_lines_01 = {
            0: 'Hello world!',
            1: 'You are a programmer?'
        }

        file_lines_02 = {
            0: 'Good morning.',
            1: 'How are you?'
        }

        lines_01_diff = self.pie.get_lines_difference(file_lines_1, file_lines_01)
        lines_02_diff = self.pie.get_lines_difference(file_lines_2, file_lines_02)

        self.assert_expected(
            value=lines_01_diff,
            expected={1: 'You are a programmer?'}
        )

        self.assert_expected(
            value=lines_02_diff,
            expected={
                1: 'How are you?',
                2: None
            }
        )


if __name__ == '__main__':
    bupytest.this()
