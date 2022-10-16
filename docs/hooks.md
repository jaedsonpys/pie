# Pie Hooks

Hooks are commands that are executed before an action is performed. If this command returns exit code 0, the action is executed, otherwise nothing happens and an error message is printed.

In Pie, hooks are stored in the `.pie/hooks.json` file, that's where you can **change and create a hook for each action**. Hooks are available for commits, adding a file and merging.