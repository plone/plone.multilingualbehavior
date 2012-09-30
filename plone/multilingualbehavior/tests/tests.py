import unittest2 as unittest
import doctest
from plone.testing import layered
from plone.multilingualbehavior.tests._testing import (
    PLONEMULTILINGUALBEHAVIOR_INTEGRATION_TESTING,
    PLONEMULTILINGUALBEHAVIOR_FUNCTIONAL_TESTING,
    optionflags,
)
integration_tests = [
    'doctest_behavior.txt',
    'doctest_native.txt',
    'doctest_grok_directive.txt'
]
functional_tests = [
    'language.txt'
]


def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite('%s' % f, \
                    package='plone.multilingualbehavior.tests',
                    optionflags=optionflags),
                 layer=PLONEMULTILINGUALBEHAVIOR_INTEGRATION_TESTING)
            for f in integration_tests]
        +
        [layered(doctest.DocFileSuite('%s' % f,
                    package='plone.multilingualbehavior.tests',
                    optionflags=optionflags),
                 layer=PLONEMULTILINGUALBEHAVIOR_FUNCTIONAL_TESTING)
            for f in functional_tests]
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
