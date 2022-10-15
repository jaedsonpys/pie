import os
import json


class Hooks(object):
    def __init__(self, hooks_filepath: str) -> None:
        self._hooks_filepath = hooks_filepath
        self.hooks = {}

        if not os.path.isfile(hooks_filepath):
            raise FileNotFoundError(f'File "{hooks_filepath}" not exists')

    def load_hooks(self) -> dict:
        with open(self._hooks_filepath, 'r') as reader:
            hooks = reader.load(reader)

        self._hooks = hooks
        return hooks
