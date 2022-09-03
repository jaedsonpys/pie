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

        with open(self.repository_info_file, 'w') as writer:
            json.dump(repository_info, writer, indent=4)

        with open(self.pieces_file, 'w') as writer:
            json.dump(pieces_object, writer, indent=4)
