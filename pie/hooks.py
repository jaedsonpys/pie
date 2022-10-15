import os
import json


class Hooks(object):
    def __init__(self, hooks_filepath: str) -> None:
        """Create a new instance of the Hook class.

        This class is responsible for loading and executing
        specific action hooks such as `commit`, `add` and
        other commands.

        :param hooks_filepath: Hooks file path.
        :type hooks_filepath: str
        :raises FileNotFoundError: If hooks file is not found.
        """

        self._hooks_filepath = hooks_filepath
        self.hooks = {}

        if not os.path.isfile(hooks_filepath):
            raise FileNotFoundError(f'File "{hooks_filepath}" not exists')

    def load_hooks(self) -> dict:
        with open(self._hooks_filepath, 'r') as reader:
            hooks = reader.load(reader)

        self._hooks = hooks
        return hooks

    def execute_hook(self, action: str) -> int:
        """Run the specified action hook script.

        :param action: Hook action
        :type action: str
        :return: Script status code.
        :rtype: int
        """

        for hook in self._hooks:
            if hook['action'] == action:
                script = hook['script']
                return os.system(script)

        return 0
