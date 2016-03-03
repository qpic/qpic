#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_qpic
----------------------------------

Tests for `qpic` module.
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

def find_test_files2(dir0, suffix0, dir1, suffix1):
    '''Search for all matching dir0/<filename>.<suffix0> and dir1/<filename>.<suffix1>.
    Typically used to find input file and expected output file.
    '''
    D = collections.defaultdict(list)
    for root, dirnames, filenames in os.walk(dir0):
        for filename in filenames:
            if '.' in filename:
                basename, suffix = filename.rsplit('.', 1)
                if suffix == suffix0:
                    D[basename].append(os.path.join(root,filename))
    for root, dirnames, filenames in os.walk(dir1):
        for filename in filenames:
            if '.' in filename:
                basename, suffix = filename.rsplit('.', 1)
                if suffix == suffix1:
                    D[basename].append(os.path.join(root,filename))
    for basename in D:
        if len(D[basename]) > 1:
            yield D[basename]

class Test_qpic(unittest.TestCase):
    pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_all_files(self):
        basenames = find_test_files2(os.path.join(TESTDIR, 'data'), 'qpic', 
                            os.path.join(TESTDIR, 'data', 'tikz'), 'tikz')
        for source_file, target_file in basenames:
            # print(source_file, target_file)
            with open(source_file) as source:
                # result = multiline_yield(qpic.main(source)) # TODO: qpic should work like this
                with Capturing() as result: # TODO: Remove hack to capture stdout
                    qpic.main(source)
                with open(target_file) as target:
                    compare = zip_longest(result, target)
                    for lineno, item in enumerate(compare):
                        self.assertEqual(item[0], item[1], '%s differs at line %d'%(target_file, lineno))

def qpic_script_test_generator(source_file, target_file):
    def test(self):
        with open(source_file) as source:
            # result = multiline_yield(qpic.main(source)) # TODO: qpic should work like this
            with Capturing() as result: # TODO: Remove hack to capture stdout
                qpic.main(source)
            with open(target_file) as target:
                compare = zip_longest(result, target)
                for lineno, item in enumerate(compare):
                    self.assertEqual(item[0], item[1], '%s differs at line %d\n%s\n%s'%(target_file, lineno, item[0], item[1]))
    return test

# Dynamic tests built from files in data/ directory

# Find all .qpic files with a matching .tikz reference file
basenames = find_test_files2(os.path.join(TESTDIR, 'data'), 'qpic', 
                    os.path.join(TESTDIR, 'data', 'tikz'), 'tikz')
# Add a test for each matching pair
for source_file, target_file in basenames:
    filename = source_file.rsplit(os.path.sep, 1)[-1]
    test_name = 'test_%s'%filename
    test = qpic_script_test_generator(source_file, target_file)
    setattr(Test_qpic, test_name, test)

if __name__ == '__main__':
    sys.exit(unittest.main())
