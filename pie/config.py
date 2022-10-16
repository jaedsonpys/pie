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
            
            with open(self._config_author_filepath, 'w') as writer:
                json.dump(author_info, writer, indent=4)
        else:
            if not os.path.isfile(self._config_author_filepath):
                with open(self._config_author_filepath, 'w') as writer:
                    json.dump(author_info, writer, indent=4)
