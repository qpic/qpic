#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tikz2pdf
----------------------------------

Tests for `tikz2pdf` module.
"""

from __future__ import print_function

try:
    # Python2
    from itertools import izip_longest as zip_longest
except ImportError:
    # Python3
    from itertools import zip_longest

import collections
import os
import os.path
import unittest

# Clever idea to capture stdout
# TODO: remove after changing qpic output to be a textstream.
from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines(True)) # True added to keep endlines
        sys.stdout = self._stdout

import qpic

# Test files are located relative to the test function being called.
TESTDIR = os.path.dirname(__file__)

def multiline_yield(textstream):
    '''Yield every text line separately, even if some text lines are multiline.
    '''
    for item in textstream:
        for line in iter(item.splitlines(True)): # True keeps endlines
            yield line

def find_test_files(dir, suffix0, suffix1):
    '''Search for all matching <filename>.<suffix0> and <filename>.<suffix1> in dir.
    Typically used to find input file and expected output file.
    '''
    D = collections.defaultdict(set)
    for root, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if '.' in filename:
                basename, suffix = filename.rsplit('.', 1)
                D[os.path.join(root, basename)].add(suffix)
    for basefile in D:
        if suffix0 in D[basefile] and suffix1 in D[basefile]:
            yield basefile

class Test_qpic(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_files(self):
        basenames = find_test_files(os.path.join(TESTDIR, 'data'), 'qpic', 'tikz')
        for basename in basenames:
            source_file = basename + '.qpic'
            target_file = basename + '.tikz'
            with open(source_file) as source:
                # result = multiline_yield(qpic.main(source)) # TODO: qpic should work like this
                with Capturing() as result: # TODO: Remove hack to capture stdout
                    qpic.main(source)
                with open(target_file) as target:
                    # compare = zip_longest(result, target)
                    # for item in compare:
                        # print(item)
                    self.assertTrue(all(a == b for a, b in zip_longest(result, target)))


if __name__ == '__main__':
    print(list(find_test_files(os.path.join(TESTDIR, 'data'), 'qpic', 'tikz')))
    import sys
    sys.exit(unittest.main())
