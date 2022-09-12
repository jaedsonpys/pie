# 0.1.0

First release of Pie, with basic functionality and no CLI usage

## Major commits

- [a691bf9](https://github.com/jaedsonpys/pie/commits/a691bf9): Adding method to create repository;
- [c8b2a26](https://github.com/jaedsonpys/pie/commits/c8b2a26): Adding method to track files;
- [a7236c2](https://github.com/jaedsonpys/pie/commits/a7236c2): Adding method to get tracked files;
- [bd752ea](https://github.com/jaedsonpys/pie/commits/bd752ea): Adding method to number file lines in a dictionary;
- [79b2183](https://github.com/jaedsonpys/pie/commits/79b2183): Adding method to get lines difference;
- [af683c1](https://github.com/jaedsonpys/pie/commits/af683c1): Adding method to create a commit object;
- [928e9c9](https://github.com/jaedsonpys/pie/commits/928e9c9): Adding method to commit file changes;
- [fc167f1](https://github.com/jaedsonpys/pie/commits/fc167f1): Adding a method to join all commits to a file.

# 0.2.0

Addition of new methods to get all commits done and get the status of files (to know if it has changed or is new).

## Major commits

- [0c965e2](https://github.com/jaedsonpys/pie/commits/0c965e2): Adding `get_commits` method to return all commits;
- [ece9bf2](https://github.com/jaedsonpys/pie/commits/ece9bf2): Removing unused variable from `_get_last_piece_hash` method;
- [9d9c05d](https://github.com/jaedsonpys/pie/commits/9d9c05d): Adding `_file_has_changed` method to check file hash;
- [87910ba](https://github.com/jaedsonpys/pie/commits/87910ba): Adding `get_files_status` to get files status.

# 0.3.0

**New functionality** to ignore files and display untracked files in the file status.

## Major commits

- [febabc5](https://github.com/jaedsonpys/pie/commits/febabc5): Removing unused import;
- [a287af4](https://github.com/jaedsonpys/pie/commits/a287af4): Adding ignore file functionality with an `.ignore` file;
- [1b49a26](https://github.com/jaedsonpys/pie/commits/1b49a26): Adding untracked files to the status of files.

# 0.4.0

Adding **new functionality** to merge files.

## Major commits

- [edfc679](https://github.com/jaedsonpys/pie/commits/edfc679): Adding `merge` method to merge files.

# 0.4.1

Fixing file not found exception when getting `.ignore` file.

## Major commits

- [3a40d64](https://github.com/jaedsonpys/pie/commits/3a40d64): Returning empty list if `.ignore` file not exists.

# 0.5.0

Optimizing the process of merging files and commiting files using threads.

## Major commits

- [48b81a2](https://github.com/jaedsonpys/pie/commits/48b81a2): Adding docstring to `get_file_status` method;
- [405126b](https://github.com/jaedsonpys/pie/commits/405126b): Using `get_tracked_files` instead of `_get_pieces_refs` method;
- [03eaf15](https://github.com/jaedsonpys/pie/commits/03eaf15): Adding `_merge_file` method and using in `merge` method;
- [d7ae041](https://github.com/jaedsonpys/pie/commits/d7ae041): Using threads to merge files;
- [4ea5c39](https://github.com/jaedsonpys/pie/commits/4ea5c39): Adding thread in `commit` method to get the difference of the files.

# 0.6.0

Changing location of author information to a file called `.author`.

## Major commits

- [48c2c1b](https://github.com/jaedsonpys/pie/commits/48c2c1b): Creating `.author` file to store author info.

# 1.0.0

Adding Command Line Interface (CLI). Fixes and new features.

## Major commits

- [3ea3b09](https://github.com/jaedsonpys/pie/commits/3ea3b09): Creating ArgEasy parser;
- [79c0e7a](https://github.com/jaedsonpys/pie/commits/79c0e7a): Using `SHA1` hash to commits ID instead of `SHA256`;
- [9bfe353](https://github.com/jaedsonpys/pie/commits/9bfe353): Creating pieces of the file only when the commit is being created;
- [00a9ed3](https://github.com/jaedsonpys/pie/commits/00a9ed3): Throwing exception if file is not being tracked;
- [b43ef0a](https://github.com/jaedsonpys/pie/commits/b43ef0a): Throwing exception if no file has been changed for commit;
- [7b7baaa](https://github.com/jaedsonpys/pie/commits/7b7baaa): Adding decorator to check repository files.

# 1.0.1

Fix documentation link in README.md

## Major commits

- [45a1bb0](https://github.com/jaedsonpys/pie/commits/45a1bb0): Fix `DOCS/` link in README.md.