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
        key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

        repository_info = {
            'author': author,
            'author_email': author_email,
            'key': key,
            'remote': None
        }

        with open(self.repository_info_file, 'w') as writer:
            json.dump(repository_info, writer, indent=4)
