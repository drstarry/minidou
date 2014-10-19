# -*- coding: utf-8 -*-
"""
Doctest runner for 'pbp.recipe.noserunner'.
"""
__docformat__ = 'restructuredtext'

import unittest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('pbp.recipe.noserunner', test)

def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../runner.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        zc.buildout.testing.normalize_path,
                        ]),
                ),
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
