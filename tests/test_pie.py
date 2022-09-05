import sys
import os
import json
import shutil

import bupytest
import utoken

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

    def test_commit(self):
        self.pie.commit(['tests/pie-test/01.txt', 'tests/pie-test/02.txt'], 'first commit')

        pieces_refs = self.pie._get_pieces_refs()
        repo_info = self.pie._get_repo_info()
        tracked_files = pieces_refs['tracked']
        commits = pieces_refs['commits']

        file_01_commits = tracked_files['tests/pie-test/01.txt']['commits']
        file_02_commits = tracked_files['tests/pie-test/02.txt']['commits']
        
        self.assert_expected(len(file_01_commits), 1)
        self.assert_expected(len(file_01_commits), 1)
        self.assert_expected(file_01_commits[0], file_02_commits[0])

        commit_info = commits[file_01_commits[0]]

        self.assert_expected(commit_info['author'], 'Jaedson')
        self.assert_expected(commit_info['author_email'], 'imunknowuser@protonmail.com')
        self.assert_expected(commit_info['message'], 'first commit')

        piece_id_01 = commit_info['files']['tests/pie-test/01.txt']
        piece_id_02 = commit_info['files']['tests/pie-test/02.txt']

        with open(f'.pie/pieces/{piece_id_01}', 'r') as reader:
            piece_token_01 = reader.read()

        with open(f'.pie/pieces/{piece_id_02}', 'r') as reader:
            piece_token_02 = reader.read()

        piece_info_01 = utoken.decode(piece_token_01, repo_info['key'])
        piece_info_02 = utoken.decode(piece_token_02, repo_info['key'])

        piece_lines_01 = piece_info_01['lines']
        piece_lines_02 = piece_info_02['lines']

        self.assert_expected(
            value=piece_lines_01,
            expected={'0': 'Hello world!'}
        )

        self.assert_expected(
            value=piece_lines_02,
            expected={
                '0': 'Good morning.',
                '1': '',
                '2': 'How are you?'
            }
        )

    def test_commit_2(self):
        with open('tests/pie-test/01.txt', 'w') as writer:
            writer.write('Hello world!\nHow are you?')

        self.pie.commit(['tests/pie-test/01.txt'], 'adding new line')

        pieces_refs = self.pie._get_pieces_refs()
        repo_info = self.pie._get_repo_info()
        tracked_files = pieces_refs['tracked']
        commits = pieces_refs['commits']

        file_01_commits = tracked_files['tests/pie-test/01.txt']['commits']
        
        self.assert_expected(len(file_01_commits), 2)
        commit_info = commits[file_01_commits[1]]

        self.assert_expected(commit_info['author'], 'Jaedson')
        self.assert_expected(commit_info['author_email'], 'imunknowuser@protonmail.com')
        self.assert_expected(commit_info['message'], 'adding new line')

        piece_id_01 = commit_info['files']['tests/pie-test/01.txt']

        with open(f'.pie/pieces/{piece_id_01}', 'r') as reader:
            piece_token_01 = reader.read()

        piece_info_01 = utoken.decode(piece_token_01, repo_info['key'])
        piece_lines_01 = piece_info_01['lines']

        # right below it is checked what has
        # been changed from the file.
        self.assert_expected(
            value=piece_lines_01,
            expected={
                '1': 'How are you?'
            }
        )

    def test_commit_3(self):
        with open('tests/pie-test/02.txt', 'w') as writer:
            writer.write('Good morning.\nHow are you?')

        self.pie.commit(['tests/pie-test/02.txt'], 'adding new line')

        pieces_refs = self.pie._get_pieces_refs()
        repo_info = self.pie._get_repo_info()
        tracked_files = pieces_refs['tracked']
        commits = pieces_refs['commits']

        file_02_commits = tracked_files['tests/pie-test/02.txt']['commits']
        
        self.assert_expected(len(file_02_commits), 2)
        commit_info = commits[file_02_commits[1]]

        self.assert_expected(commit_info['author'], 'Jaedson')
        self.assert_expected(commit_info['author_email'], 'imunknowuser@protonmail.com')
        self.assert_expected(commit_info['message'], 'adding new line')

        piece_id_02 = commit_info['files']['tests/pie-test/02.txt']

        with open(f'.pie/pieces/{piece_id_02}', 'r') as reader:
            piece_token_02 = reader.read()

        piece_info_02 = utoken.decode(piece_token_02, repo_info['key'])
        piece_lines_02 = piece_info_02['lines']

        # right below it is checked what has
        # been changed from the file.
        self.assert_expected(
            value=piece_lines_02,
            expected={
                '1': 'How are you?',
                '2': None
            }
        )


if __name__ == '__main__':
    bupytest.this()
