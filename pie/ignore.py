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


def remove_slash(string: str) -> str:
    if string[-1::] == '/':
        return string[:-1]
    else:
        return string


def get_ignored_files() -> list:
    ignored_files = []

    if os.path.isfile('.ignore'):
        with open('.ignore', 'r') as reader:
            ignored_files = [i.replace('\n', '') for i in reader.readlines()]
            ignored_files = [i.replace('./', '') for i in ignored_files]
            ignored_files = list(map(remove_slash, ignored_files))

    ignored_files.append('.pie')
    ignored_files.append('venv')

    return ignored_files


def get_not_ignored_files() -> list:
    ignored_files = get_ignored_files()

    all_files = []
    not_ignored = []
    filtered_files = []

    for dirpath, dirs, files in os.walk('./'):
        dirpath = dirpath.replace('./', '')

        for file in files:
            all_files.append(os.path.join(dirpath, file))

        for dir in dirs:
            all_files.append(os.path.join(dirpath, dir))

    for file in all_files:
        first_path = file.split('/')[0]
        if file not in ignored_files and first_path not in ignored_files:
            not_ignored.append(file)

    # in the code below, we ignore files that have the text
    # specified in the .ignore file in the format starting with "*"

    ext_ignore = [i.replace('*', '') for i in ignored_files if i.startswith('*')]

    for file in not_ignored:
        for ext in ext_ignore:
            if not ext in file:
                filtered_files.append(file)
                break

    return filtered_files or not_ignored
