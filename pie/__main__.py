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

from .__init__ import __version__
from . import pie

from argeasy import ArgEasy


def main() -> int:
    parser = ArgEasy(
        name='pie',
        description='Pie, a complete version control',
        version=__version__
    )

    parser.add_argument('init', 'Create a new repository', action='store_true')
    parser.add_argument('status', 'Gets status of the files', action='store_true')
    parser.add_argument('merge', 'Merges all committed files', action='store_true')
    parser.add_argument('log', 'Prints all performed commits', action='store_true')

    parser.add_argument('add', 'Adds a new file to the trace tree', action='append')
    parser.add_argument('commit', 'Commit a file added to the trace tree', action='append')
