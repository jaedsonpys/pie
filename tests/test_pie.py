import sys
import os
import json

import bupytest

sys.path.insert(0, './')
from pie import pie


class TestPie(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.pie = pie.Pie()


if __name__ == '__main__':
    bupytest.this()
