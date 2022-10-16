# Pie Hooks

Hooks are commands that are executed before an action is performed. If this command returns exit code 0, the action is executed, otherwise nothing happens and an error message is printed.

In Pie, hooks are stored in the `.pie/hooks.json` file, that's where you can **change and create a hook for each action**. Hooks are available for commits, adding a file and merging.

## Creating a hook

To create a hook, you should first understand the simple structure of the `.pie/hooks.json` file:

```json
[
    {
        "action": "commit",
        "script": "echo Hello"
    }
]
```

- action: Name of the action that runs this hook, for commits the action name is `commit`, for adding files the action name is `track-file`, and for merges the action name is `merge`;
- script: Command to be executed. If you want to run multiple commands from a file, use `./script.sh`.

With that, you add the hooks in object format inside the list in the JSON, like this:

```json
[
    {
        "action": "commit",
        "script": "./unit_test.sh"
    },
    {
        "action": "track-file",
        "script": "echo TrakFile"
    },
    {
        "action": "merge",
        "script": "echo \"Merge this!\""
    }
]
```