import unittest2 as unittest
import doctest
from plone.testing import layered
from plone.multilingualbehavior.testing import PLONEMULTILINGUALBEHAVIOR_INTEGRATION_TESTING
from plone.multilingualbehavior.testing import PLONEMULTILINGUALBEHAVIOR_FUNCTIONAL_TESTING
from plone.multilingualbehavior.testing import optionflags

import pkg_resources


integration_tests = [
    'doctest_behavior.txt',
    'doctest_native.txt',
    'doctest_grok_directive.txt',
    'doctest_manualbehavior.txt',
]
functional_tests = [
    'language.txt'
]


def is_plone43():
    plone_pkg = pkg_resources.get_distribution('Products.CMFPlone')
    return cmp(pkg_resources.parse_version(plone_pkg.version),
               pkg_resources.parse_version('4.3')) >= 0


def test_suite():
    if not is_plone43():
        # This test doesn't work for versions for Dexterity under 2.0
        # For testing purposes, we only test for the Plone version is
        # superior to 4.3 as this is the fixture being tested.
        integration_tests.remove('doctest_manualbehavior.txt')

    return unittest.TestSuite(
        [layered(doctest.DocFileSuite('%s' % f,
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
