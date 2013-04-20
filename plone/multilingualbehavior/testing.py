# -*- coding: utf-8 -*-
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from zope.configuration import xmlconfig
from OFS.Folder import Folder
from Testing import ZopeTestCase as ztc

import doctest
import transaction


class PloneMultilingualbehaviorLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.multilingualbehavior
        import plone.multilingualbehavior.tests
        xmlconfig.file('configure.zcml', plone.multilingualbehavior,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', plone.multilingualbehavior.tests,
                       context=configurationContext)

        # Support sessionstorage in tests
        app.REQUEST['SESSION'] = self.Session()
        if not hasattr(app, 'temp_folder'):
            tf = Folder('temp_folder')
            app._setObject('temp_folder', tf)
            transaction.commit()

        ztc.utils.setupCoreSessions(app)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.multilingualbehavior:default')
        applyProfile(portal, 'plone.multilingualbehavior.tests:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])


PLONEMULTILINGUALBEHAVIOR_FIXTURE = PloneMultilingualbehaviorLayer()

PLONEMULTILINGUALBEHAVIOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEMULTILINGUALBEHAVIOR_FIXTURE,),
    name="plone.multilingualbehavior:Integration")
PLONEMULTILINGUALBEHAVIOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEMULTILINGUALBEHAVIOR_FIXTURE,),
    name="plone.multilingualbehavior:Functional")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
