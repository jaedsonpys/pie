import os
import json


class PieConfig(object):
    def __init__(self) -> None:
        self._home_dirpath = os.path.expanduser('~')
        self._config_dirpath = os.path.join(self._home_dirpath, '.pie-config')
        self._config_author_filepath = os.path.join(self._config_dirpath, 'author.json')

        if not os.path.isdir(self._config_dirpath):
            os.mkdir(self._config_dirpath)
            self.write_author_info(author=None, author_email=None)  
        else:
            if not os.path.isfile(self._config_author_filepath):
                self.write_author_info(author=None, author_email=None)  

    def write_author_info(self, author: str, author_email: str) -> None:
        """Write author name and author email
        in `.pie-config` directory.

        :param author: Author name.
        :type author: str
        :param author_email: Author email.
        :type author_email: str
        """

        author_info = {
            'author': author,
            'author_email': author_email
        }

        with open(self._config_author_filepath, 'w') as writer:
            json.dump(author_info, writer, indent=4)

    def get_author_info(self) -> dict:
        """Get author information in a
        dictionary.

        :return: Author information
        :rtype: dict
        """

        with open(self._config_author_filepath, 'r') as reader:
            author = json.load(reader)

        return author
