import os
import json
from types import FunctionType

from . import exceptions


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

        if not os.path.isfile(hooks_filepath):
            raise FileNotFoundError(f'File "{hooks_filepath}" not exists')

    def _load_hooks(self) -> dict:
        with open(self._hooks_filepath, 'r') as reader:
            hooks = json.load(reader)

        return hooks

    def run_hook(self, action: str) -> FunctionType:
        """Run the specified action hook script.

        :param action: Hook action
        :type action: str
        :return: Script status code.
        :rtype: int
        """

        def check_hook(func):
            def decorator(*args, **kwargs):
                for hook in self._load_hooks():
                    if hook['action'] == action:
                        script = hook['script']
                        code = os.system(script)

                        if code == 0:
                            return func(*args, **kwargs)
                        else:
                            raise exceptions.HookFailedError(f'Hook to "{hook["action"]}" failed.')

                return func(*args, **kwargs)

            return decorator

        return check_hook
