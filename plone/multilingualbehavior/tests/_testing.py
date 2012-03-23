# -*- coding: utf-8 -*-
import doctest
from plone.app.testing import (
    PLONE_FIXTURE,
    PloneSandboxLayer,
    applyProfile,
    setRoles,
    TEST_USER_ID,
    IntegrationTesting,
    FunctionalTesting,
)
from zope.configuration import xmlconfig

class PloneMultilingualbehaviorLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.multilingualbehavior
        import plone.multilingualbehavior.tests
        xmlconfig.file('configure.zcml', plone.multilingualbehavior,
                        context=configurationContext)
        xmlconfig.file('configure.zcml', plone.multilingualbehavior.tests,
                        context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.multilingualbehavior:default')
        applyProfile(portal, 'plone.multilingualbehavior.tests:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])


PLONEMULTILINGUALBEHAVIOR_FIXTURE = PloneMultilingualbehaviorLayer()

PLONEMULTILINGUALBEHAVIOR_INTEGRATION_TESTING = IntegrationTesting(\
    bases=(PLONEMULTILINGUALBEHAVIOR_FIXTURE,),\
    name="plone.multilingualbehavior:Integration")
PLONEMULTILINGUALBEHAVIOR_FUNCTIONAL_TESTING = FunctionalTesting(\
    bases=(PLONEMULTILINGUALBEHAVIOR_FIXTURE,),\
    name="plone.multilingualbehavior:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
