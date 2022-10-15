import os
import json


class Hooks(object):
    def __init__(self, hooks_filepath: str) -> None:
        self._hooks_filepath = hooks_filepath
