# Pie, a version control
# Copyright (C) 2022  Jaedson Silva

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json

import os
import secrets
import hashlib

from . import exceptions


class Pie(object):
    def __init__(self) -> None:
        """Creating a new instance from Pie."""

        self.repository_path = os.path.join(os.getcwd(), '.pie')
        self.repository_info_file = os.path.join(self.repository_path, '.info')
        self.pieces_file = os.path.join(self.repository_path, 'pieces.json')
        self.pieces_dir = os.path.join(self.repository_path, 'pieces')

    def _get_repo_info(self) -> dict:
        with open(self.repository_info_file, 'r') as reader:
            repo_info = json.load(reader)

        return repo_info

    def _get_pieces_refs(self) -> dict:
        with open(self.pieces_file, 'r') as reader:
            pieces_refs = json.load(reader)

        return pieces_refs

    def _write_repo_info(self, repository_info: dict) -> None:
        with open(self.repository_info_file, 'w') as writer:
            json.dump(repository_info, writer, indent=4)

    def _write_pieces_refs(self, pieces_refs: dict) -> None:
        with open(self.pieces_file, 'w') as writer:
            json.dump(pieces_refs, writer, indent=4)

    def _get_file_hash(self, filepath: str) -> str:
        with open(filepath, 'rb') as reader:
            content = reader.read()

        return hashlib.md5(content).hexdigest()

    def create_repository(self, author: str, author_email: str) -> None:
        """Create a new repository.

        :param author: Commits author.
        :type author: str
        :param author_email: Email of commits author.
        :type author_email: str
        :raises exceptions.RepositoryExistsError: Thrown if repository already exists.
        """

        if os.path.isdir(self.repository_path):
            raise exceptions.RepositoryExistsError(f'Repository exists in "{self.repository_path}"')

        os.mkdir(self.repository_path)
        os.mkdir(self.pieces_dir)

        key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

        repository_info = {
            'author': author,
            'author_email': author_email,
            'key': key,
            'remote': None
        }

        pieces_object = {
            'tracked': {},
            'commits': {}
        }

        self._write_repo_info(repository_info)
        self._write_pieces_refs(pieces_object)

    def get_tracked_files(self) -> dict:
        pieces_refs = self._get_pieces_refs()
        return pieces_refs['tracked']

    def track_file(self, filepath: str) -> None:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'File "{filepath}" not found')

        file_info = {
            'filename': filepath,
            'hash': self._get_file_hash(filepath)
        }

        pieces_refs = self._get_pieces_refs()
        pieces_refs['tracked'][filepath] = file_info

        self._write_pieces_refs(pieces_refs)

    def index_file_lines(self, filepath: str) -> dict:
        with open(filepath, 'r') as reader:
            file = reader.readlines()

        file_lines = {}

        for line, text in enumerate(file):
            if text[-1::] == '\n':
                text = text[:-1]

            file_lines[line] = text

        return file_lines

    def get_lines_difference(self, previous_lines: dict, current_lines: dict) -> dict:
        diff = {}

        # the following loop is needed to "remove" the
        # lines that have been removed from the current file

        for line, text in previous_lines.items():
            current_line = current_lines.get(line)

            if current_line is None:
                diff[line] = None
            elif current_line != text:
                diff[line] = text

        # the loop below is needed to get new rows
        # added that were not found in the first loop

        for line, text in current_lines.items():
            previous_line = previous_lines.get(line)

            if previous_line is None:
                diff[line] = text
            elif previous_line != text:
                diff[line] = text

        return diff
