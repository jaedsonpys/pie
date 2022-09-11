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

from argeasy import ArgEasy

from . import exceptions
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

    parser.add_argument('add', 'Adds a new file to the trace tree', action='append')
    parser.add_argument('commit', 'Commit a file added to the trace tree', action='append')

    # commit and file tracking
    parser.add_flag('-m', 'Adds a message to the commit')
    # parser.add_flag('-a', 'Selects all tracked files', action='store_true')
    # parser.add_flag('-A', 'Selects all files in the directory', action='store_true')

    # config
    parser.add_flag('--author', 'Repository author')
    parser.add_flag('--author-email', 'Repository author email')

    args = parser.parse()
    pie = Pie()

    # creating repository
    if args.init:
        author = args.author
        author_email = args.authoremail

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
            elif args.add:
                files = args.add

                for file in files:
                    try:
                        pie.track_file(file)
                    except FileNotFoundError:
                        print(f'\033[31merror: file "{file}" not found')
                        return 1
            elif args.commit:
                files = args.commit
                message = args.m

                if not message:
                    print('\033[33ma message to describe your commit is required.\033[m')
                    print('(use the "-m" flag to set your message/description)')
                    return 1

                try:
                    commit, commit_hash = pie.commit(files, message)
                except exceptions.NoFilesToCommitError:
                    print('no changed files, commit cancelled')
                    return 1

                print(f'\033[1m\033[4;33m[{commit_hash[:8]}]\033[m {commit["message"]}')
                print(f'  {len(commit["files"])} files were modified')
        except exceptions.RepositoryNotExistsError:
            print('\033[31merror: no ".pie" repository found in this directory\033[m')
            return 1

    return 0
