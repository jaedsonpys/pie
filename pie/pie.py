import json

import os
import secrets
import hashlib

from . import exceptions


class Pie(object):
    def create_repository(self, author: str, author_email: str) -> None:
        """Create a new repository.

        :param author: Commits author.
        :type author: str
        :param author_email: Email of commits author.
        :type author_email: str
        :raises exceptions.RepositoryExistsError: Thrown if repository already exists.
        """

        repository_path = os.path.join(os.getcwd(), '.pie')

        if os.path.isdir(repository_path):
            raise exceptions.RepositoryExistsError(f'Repository exists in "{repository_path}"')

        os.mkdir(repository_path)
        key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

        repository_info = {
            'author': author,
            'author_email': author_email,
            'key': key,
            'remote': None
        }

        repository_info_file = os.path.join(repository_path, '.info')

        with open(repository_info_file, 'w') as writer:
            json.dump(repository_info, writer, indent=4)
