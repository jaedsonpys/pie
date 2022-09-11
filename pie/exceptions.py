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


class RepositoryExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class CommitIntegrityError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FileNotTrackedError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoFilesToCommitError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RepositoryNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
