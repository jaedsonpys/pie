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

        if not os.path.isfile(hooks_filepath):
            raise FileNotFoundError(f'File "{hooks_filepath}" not exists')

    def _load_hooks(self) -> dict:
        with open(self._hooks_filepath, 'r') as reader:
            hooks = json.load(reader)

        return hooks

    def execute_hook(self, action: str) -> int:
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
                            return False

                return func(*args, **kwargs)

            return decorator

        return check_hook
