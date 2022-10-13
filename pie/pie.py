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

from functools import wraps
import hashlib
import json
import os
import secrets
from concurrent import futures
from datetime import datetime
from typing import List, Union

import utoken

from . import exceptions
from .ignore import get_not_ignored_files


def repo_required(method):
    @wraps(method)
    def decorator(ref, *args, **kwargs):
        if not ref.check_repo_files():
            raise exceptions.RepositoryNotExistsError('Repository not exists')
        else:
            return method(ref, *args, **kwargs)
    
    return decorator


class Pie(object):
    def __init__(self) -> None:
        """Creating a new instance from Pie."""

        self.repository_path = os.path.join(os.getcwd(), '.pie')
        self.repository_info_file = os.path.join(self.repository_path, '.info')
        self.author_info_file = os.path.join(self.repository_path, '.author')
        self.pieces_file = os.path.join(self.repository_path, 'pieces.json')
        self.pieces_dir = os.path.join(self.repository_path, 'pieces')

    def check_repo_files(self) -> bool:
        """Checks all files in the repository
        and returns `True` if all are present.

        :return: True if all are present.
        :rtype: bool
        """

        files = [
            os.path.isdir(self.repository_path),
            os.path.isfile(self.repository_info_file),
            os.path.isfile(self.author_info_file),
            os.path.isdir(self.pieces_dir),
            os.path.isfile(self.pieces_file),
        ]

        return all(files)

    @repo_required
    def _get_repo_info(self) -> dict:
        with open(self.repository_info_file, 'r') as reader:
            repo_info = json.load(reader)

        return repo_info

    @repo_required
    def _get_pieces_refs(self) -> dict:
        with open(self.pieces_file, 'r') as reader:
            pieces_refs = json.load(reader)

        return pieces_refs

    @repo_required
    def _get_author_info(self) -> dict:
        with open(self.author_info_file, 'r') as reader:
            author_info = json.load(reader)

        return author_info

    def _write_repo_info(self, repository_info: dict) -> None:
        with open(self.repository_info_file, 'w') as writer:
            json.dump(repository_info, writer, indent=4)

    def _write_pieces_refs(self, pieces_refs: dict) -> None:
        with open(self.pieces_file, 'w') as writer:
            json.dump(pieces_refs, writer, indent=4)

    def _write_author_info(self, author: str, author_email: str) -> None:
        with open(self.author_info_file, 'w') as writer:
            author_info = {
                'author': author, 'author_email': author_email
            }

            json.dump(author_info, writer, indent=4)

    def _get_file_hash(self, filepath: str) -> str:
        with open(filepath, 'rb') as reader:
            content = reader.read()

        return hashlib.md5(content).hexdigest()

    def create_repository(self, author: str, author_email: str) -> None:
        """Create a new repository.

        :param author: Commits author.
        :type author: str
        :param author_email: Email of commits author.
        :type author_email: str
        :raises exceptions.RepositoryExistsError: Thrown if repository already exists.
        """

        if os.path.isdir(self.repository_path):
            raise exceptions.RepositoryExistsError(f'Repository exists in "{self.repository_path}"')

        os.mkdir(self.repository_path)
        os.mkdir(self.pieces_dir)

        key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

        repository_info = {
            'key': key,
            'remote': None
        }

        pieces_object = {
            'tracked': {},
            'commits': {}
        }

        self._write_repo_info(repository_info)
        self._write_pieces_refs(pieces_object)
        self._write_author_info(author, author_email)

    @repo_required
    def get_tracked_files(self) -> dict:
        """Get the tracked files

        :return: Returns a dictionary with the
        tracked file information.
        :rtype: dict
        """

        pieces_refs = self._get_pieces_refs()
        return pieces_refs['tracked']

    @repo_required
    def track_file(self, filepath: str) -> None:
        """Adds a new file to the trace.

        :param filepath: File path.
        :type filepath: str
        :raises FileNotFoundError: If the file is not found.
        """

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'File "{filepath}" not found')

        if './' not in filepath:
            filepath = os.path.join('.', filepath)

        pieces_refs = self._get_pieces_refs()

        if filepath not in pieces_refs['tracked']:
            file_info = {
                'filename': filepath,
                'commits': []
            }

            pieces_refs['tracked'][filepath] = file_info
            self._write_pieces_refs(pieces_refs)

    def index_file_lines(self, filepath: str) -> dict:
        """Numbers the lines of the file in a dictionary

        :param filepath: File path.
        :type filepath: str
        :return: Return the file lines.
        :rtype: dict
        """

        with open(filepath, 'r') as reader:
            file = reader.readlines()

        file_lines = {}

        # removing "\n" only from the end of the line
        for line, text in enumerate(file):
            if text[-1::] == '\n':
                text = text[:-1]

            file_lines[line] = text

        return file_lines

    def get_lines_difference(self, previous_lines: dict, current_lines: dict) -> dict:
        """Gets the difference between two
        dictionaries with numbered lines.

        If there is a `None` value, it means
        that the line has been deleted.

        :param previous_lines: Preivous lines.
        :type previous_lines: dict
        :param current_lines: Current lines.
        :type current_lines: dict
        :return: Returns the difference between the two dictionaries.
        :rtype: dict
        """

        diff = {}

        # the following loop is needed to "remove" the
        # lines that have been removed from the current file

        for line, text in previous_lines.items():
            current_line = current_lines.get(line)

            if current_line is None:
                diff[line] = None
            elif current_line != text:
                diff[line] = text

        # the loop below is needed to get new rows
        # added that were not found in the first loop

        for line, text in current_lines.items():
            previous_line = previous_lines.get(line)

            if previous_line is None:
                diff[line] = text
            elif previous_line != text:
                diff[line] = text

        return diff

    def _join_file_lines(self, previous_lines: dict, current_lines: dict) -> dict:
        for line, text in current_lines.items():
            line = int(line)

            if text == None:
                previous_lines.pop(line)
            else:
                previous_lines[line] = text

        return previous_lines

    def _decode_piece_token(self, piece_token: str) -> dict:
        integrity_exceptions = (
            utoken.exceptions.InvalidContentTokenError,
            utoken.exceptions.InvalidKeyError,
            utoken.exceptions.InvalidTokenError
        )

        try:
            piece_info = utoken.decode(piece_token, self._get_repo_info()['key'])
        except integrity_exceptions:
            raise exceptions.CommitIntegrityError('Broken commit integrity')

        return piece_info

    @repo_required
    def join_file_changes(self, filepath: str) -> dict:
        """Merge all committed changes from the
        file into a single dictionary with numbered lines.

        :param filepath: Path of the file to be merged
        :type filepath: str
        :raises exceptions.CommitIntegrityError: If the commits have been
        altered by a third party, the integrity is broken.
        :return: Merged lines.
        :rtype: dict
        """

        pieces_refs = self._get_pieces_refs()
        file = pieces_refs['tracked'][filepath]

        commits = pieces_refs['commits']
        previous_piece_hash = 0
        previous_lines = {}

        for commit_id in file['commits']:
            commit_info = commits[commit_id]
            piece_id = commit_info['files'][filepath]
            piece_filepath = os.path.join(self.pieces_dir, piece_id)

            with open(piece_filepath, 'r') as reader:
                piece_token = reader.read()

            piece_info = self._decode_piece_token(piece_token)

            if piece_info['previous_hash'] == previous_piece_hash:
                piece_json = json.dumps(piece_info).encode()
                piece_hash = hashlib.sha256(piece_json).hexdigest()

                previous_piece_hash = piece_hash
            else:
                raise exceptions.CommitIntegrityError('Broken commit integrity')

            previous_lines = self._join_file_lines(previous_lines, piece_info['lines'])

        return previous_lines

    def get_file_difference(self, filepath: str) -> dict:
        with futures.ThreadPoolExecutor() as executor:
            th1 = executor.submit(self.join_file_changes, filepath)
            th2 = executor.submit(self.index_file_lines, filepath)

            previous_lines = th1.result()
            current_lines = th2.result()

        lines_difference = self.get_lines_difference(previous_lines, current_lines)
        return lines_difference

    @repo_required
    def _create_commit(self, files_refs: dict, message: str) -> Union[dict, str]:
        author_info = self._get_author_info()
        pieces_refs = self._get_pieces_refs()

        files = {}

        for file, info in files_refs.items():
            files[file] = self._create_piece(info['previous_hash'], info['diff'])

        commit = {
            'author': author_info['author'],
            'author_email': author_info['author_email'],
            'message': message,
            'datetime': datetime.now().strftime('%Y.%m.%d %H:%M:%S'),
            'files': files
        }

        commit_json = json.dumps(commit).encode()
        commit_hash = hashlib.sha1(commit_json).hexdigest()

        for file in files_refs:
            pieces_refs['tracked'][file]['commits'].append(commit_hash)

        pieces_refs['commits'][commit_hash] = commit
        self._write_pieces_refs(pieces_refs)

        return commit, commit_hash

    @repo_required
    def _create_piece(self, previous_hash: str, lines: dict) -> str:
        repo_info = self._get_repo_info()

        piece_info = {
            'previous_hash': previous_hash,
            'lines': lines,
        }

        piece_info = utoken.encode(piece_info, repo_info['key'])

        piece_id = hashlib.md5(secrets.token_bytes(32)).hexdigest()
        piece_path = os.path.join(self.pieces_dir, piece_id)

        with open(piece_path, 'w') as writer:
            writer.write(piece_info)

        return piece_id

    @repo_required
    def _get_last_piece_hash(self, filepath: str) -> str:
        pieces_refs = self._get_pieces_refs()
        file = pieces_refs['tracked'][filepath]

        commits = pieces_refs['commits']
        last_commit_id = file['commits'][-1]

        commit_info = commits[last_commit_id]
        piece_id = commit_info['files'][filepath]
        piece_filepath = os.path.join(self.pieces_dir, piece_id)

        with open(piece_filepath, 'r') as reader:
            piece_token = reader.read()

        piece_info = self._decode_piece_token(piece_token)
        piece_json = json.dumps(piece_info).encode()

        return hashlib.sha256(piece_json).hexdigest()

    @repo_required
    def get_commits(self) -> dict:
        """Return all commits.

        :return: Commits in a dict.
        :rtype: dict
        """

        pieces_refs = self._get_pieces_refs()
        return pieces_refs['commits']

    def file_has_changed(self, filepath: str) -> bool:
        previous_file_lines = self.join_file_changes(filepath)
        current_file_lines = self.index_file_lines(filepath)

        previous_file_lines_json = json.dumps(previous_file_lines).encode()
        previous_hash = hashlib.md5(previous_file_lines_json).hexdigest()

        current_file_lines_json = json.dumps(current_file_lines).encode()
        current_hash = hashlib.md5(current_file_lines_json).hexdigest()

        return previous_hash != current_hash

    @repo_required
    def get_files_status(self) -> List[dict]:
        """Returns the status of new, uncommitted and
        untracked files (as long as they are not in the .ignore file).

        :return: Files status
        :rtype: List[dict]
        """

        tracked_files = self.get_tracked_files()
        files_status = []

        for filepath, info in tracked_files.items():
            if not info['commits']:
                files_status.append({
                    'filepath': filepath,
                    'status': 'new'
                })
            else:
                file_has_changed = self.file_has_changed(filepath)
                
                if file_has_changed:
                    files_status.append({
                        'filepath': filepath,
                        'status': 'uncommitted'
                    })

        not_ignored_files = get_not_ignored_files()

        for filepath in not_ignored_files:
            filepath = os.path.join('.', filepath)

            if filepath not in tracked_files.keys():
                files_status.append({
                    'filepath': filepath,
                    'status': 'untracked'
                })

        return files_status

    @repo_required
    def commit(self, filepath_list: list, message: str) -> Union[dict, str]:
        """Commit the files.

        :param filepath_list: List of files that have changed.
        :type filepath_list: list
        :param message: Commit message.
        :type message: str
        :return: Return the commit data.
        :rtype: Union[dict, str]
        """

        tracked_files = self.get_tracked_files()
        file_refs = {}

        for filepath in filepath_list:
            if './' not in filepath:
                filepath = os.path.join('.', filepath)

            file_info = tracked_files.get(filepath)

            if file_info:
                if not file_info['commits']:
                    file_refs[filepath] = {
                        'diff': self.index_file_lines(filepath),
                        'previous_hash': 0
                    }
                elif self.file_has_changed(filepath):
                    previous_hash = self._get_last_piece_hash(filepath)
                    lines_difference = self.get_file_difference(filepath)

                    if lines_difference:
                        file_refs[filepath] = {
                            'diff': lines_difference,
                            'previous_hash': previous_hash
                        }
            else:
                raise exceptions.FileNotTrackedError(f'File "{filepath}" not tracked')

        if not file_refs:
            raise exceptions.NoFilesToCommitError('No files to commit')

        return self._create_commit(file_refs, message)

    def _merge_file(self, filepath: str) -> Union[bool, str]:
        difference = self.get_file_difference(filepath)

        if difference:
            versioned_file = self.join_file_changes(filepath)

            with open(filepath, 'w') as writer:
                writer.write('\n'.join(versioned_file.values()))

            return filepath
        else:
            return False

    @repo_required
    def merge(self) -> list:
        """Merge all committed files.

        Creates the file if it does not exist
        and changes the current contents of a file
        that is being merged.

        :return: Returns a list with the files that have been merged.
        :rtype: list
        """

        tracked_files = self.get_tracked_files()
        merged_files = []

        # def callback(fn: futures.Future):
        #     result = fn.result()
        #     if result:
        #         merged_files.append(result)

        with futures.ThreadPoolExecutor() as executor:
            threads = []

            for filepath in tracked_files.keys():
                future = executor.submit(self._merge_file, filepath)
                future.add_done_callback(lambda fn: merged_files.append(fn.result()) if fn.result() else None)
                threads.append(future)

            while not all([i.done() for i in threads]):
                pass

        return merged_files
