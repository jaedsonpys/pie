import os
import json


class PieConfig(object):
    def __init__(self) -> None:
        self._home_dirpath = os.path.expanduser('~')
        self._config_dirpath = os.path.join(self._home_dirpath, '.pie-config')
        self._config_author_filepath = os.path.join(self._config_dirpath, 'author.json')

        author_info = {
            'author': None,
            'author_email': None
        }

        if not os.path.isdir(self._pie_config_dirpath):
            os.mkdir(self._pie_config_dirpath)
            self.write_author_info(author_info)  
        else:
            if not os.path.isfile(self._config_author_filepath):
                self.write_author_info(author_info)

    def write_author_info(self, author_info: dict) -> None:
        with open(self._config_author_filepath, 'w') as writer:
            json.dump(author_info, writer, indent=4)
