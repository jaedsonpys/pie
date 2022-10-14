# Pie, a version control
# Copyright (C) 2022  Jaedson Silva

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from argeasy import ArgEasy

from . import exceptions, ignore
from .__init__ import __version__
from .pie import Pie


def main() -> int:
    parser = ArgEasy(
        name='pie',
        description='Pie, a complete version control',
        version=__version__
    )

    parser.add_argument('init', 'Create a new repository', action='store_true')
    parser.add_argument('status', 'Gets status of the files', action='store_true')
    # parser.add_argument('merge', 'Merges all committed files', action='store_true')
    parser.add_argument('log', 'Prints all performed commits', action='store_true')
    parser.add_argument('diff', 'Get files difference', action='store_true')

    parser.add_argument('add', 'Adds a new file to the trace tree', action='append')
    parser.add_argument('commit', 'Commit a file added to the trace tree', action='append')

    # commit and file tracking
    parser.add_flag('-m', 'Adds a message to the commit')
    parser.add_flag('-am', 'Select all tracked files and set a commit message')

    parser.add_flag('-a', 'Selects all tracked files to commit', action='store_true')
    parser.add_flag('-A', 'Selects all files in the directory to track', action='store_true')

    # config
    parser.add_flag('--author', 'Repository author')
    parser.add_flag('--author-email', 'Repository author email')

    args = parser.parse()
    pie = Pie()

    # creating repository
    if args.init:
        author = args.author
        author_email = args.author_email

        if not author or not author_email:
            print('\033[31merror: use the "--author" and "--author-email" flag to set the author information\033[m')
            return 1

        try:
            pie.create_repository(author, author_email)
        except exceptions.RepositoryExistsError:
            print('\033[31merror: a repository already exists in this directory\033[m')
            return 1
    else:
        try:
            if args.status:  # print files status
                status = pie.get_files_status()

                if not status:
                    print('No uncommitted files, untracked files or new files in the current directory')
                    return 0

                uncommitted = [i for i in status if i['status'] == 'uncommitted']
                untracked = [i for i in status if i['status'] == 'untracked']
                new_files = [i for i in status if i['status'] == 'new']

                if new_files:
                    print('newly added files, but not yet committed.')
                    print('  (use "pie commit" argument to commit files):\n')

                    for file in new_files:
                        print(f'    \033[32m{file["filepath"]}\033[m')

                    print()

                if uncommitted:
                    print('uncommitted files.')
                    print('  (use "pie commit" argument to commit files):\n')

                    for file in uncommitted:
                        print(f'    \033[32m{file["filepath"]}\033[m')

                    print()

                if untracked:
                    print('not added files that can be tracked.')
                    print('  (use "pie add" argument to add files):\n')

                    for file in untracked:
                        print(f'    \033[31m{file["filepath"]}\033[m')

                    print()
            elif args.log:
                commits = pie.get_commits()

                for commit_id, info in commits.items():
                    author = info['author']
                    author_email = info['author_email']

                    print(f'\033[33m{commit_id}\033[m ({author} <\033[32m{author_email}\033[m>)')
                    print(f'Date: {info["datetime"]}')
                    print(f'Changed files: {len(info["files"])}\n')
                    print(f'    {info["message"]}\n')
            elif args.add is not None:
                files_to_add = args.add
                all_files_flag = args.A

                tracked_info = pie.get_tracked_files()
                tracked_files = tracked_info.keys()

                if all_files_flag:
                    not_ignored_files = ignore.get_not_ignored_files()
                    for file in not_ignored_files:
                        file = os.path.join('.', file)
                        if file not in tracked_files:
                            files_to_add.append(file)

                if not files_to_add:
                    print('\033[31merror: no file specified to track (use "pie add" argument and '
                          'pass a list of files or use the "-A" flag to select all files)\033[m')
                    return 1

                for file in files_to_add:
                    try:
                        pie.track_file(file)
                    except FileNotFoundError:
                        print(f'\033[31merror: file "{file}" not found')
                        return 1
            elif args.commit is not None:
                files = args.commit
                message = args.m
                all_tracked_files_flag = args.a

                if args.am:
                    message = args.am
                    all_tracked_files_flag = True

                if all_tracked_files_flag:
                    tracked_info = pie.get_tracked_files()

                    for filepath in tracked_info.keys():
                        if pie.file_has_changed(filepath):
                            files.append(filepath)

                if not message:
                    print('\033[33ma message to describe your commit is required.\033[m')
                    print('(use the "-m" flag to set your message/description)')
                    return 1

                try:
                    commit, commit_hash = pie.commit(files, message)
                except exceptions.NoFilesToCommitError:
                    print('no changed files, commit cancelled')
                    return 1
                except exceptions.FileNotTrackedError as err:
                    print(f'\033[31m{err.args[0]}\033[m')
                    print('(use "pie add" argument to add files)')
                    return 1

                print(f'\033[1m\033[4;33m[{commit_hash[:8]}]\033[m {commit["message"]}')
                print(f'  {len(commit["files"])} files were modified')
            elif args.diff:
                print('View difference between last commits and current file')
                print('  (use "pie commit" argument to commit files):\n')

                tracked_files = pie.get_tracked_files()

                for filepath in tracked_files.keys():
                    current_lines = pie.index_file_lines(filepath)
                    previous_lines = pie.join_file_changes(filepath)
                    difference = pie.get_lines_difference(previous_lines, current_lines)

                    if difference:
                        lines_number = len(current_lines) - len(previous_lines)

                        if lines_number < 0:
                            lines_status = f'\033[31m  --{lines_number * -1} line(s) removed\033[m\n'
                        else:
                            lines_status = f'\033[32m  ++{lines_number} line(s) added\033[m\n'

                        print(f'  {filepath}')
                        print(lines_status)
                        for number, line in difference.items():
                            print(f'\033[33m    {number} | {line}')

                        print('\033[m')
        except exceptions.RepositoryNotExistsError:
            print('\033[31merror: no ".pie" repository found in this directory\033[m')
            return 1

    return 0
