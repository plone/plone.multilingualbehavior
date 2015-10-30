# -*- coding: utf-8 -*-
from Products.GenericSetup.utils import _resolveDottedName
from zope.component.hooks import getSite
from zope.component.interfaces import IComponentRegistry
from zope.component import getGlobalSiteManager
import transaction
import logging
from Products.CMFCore.utils import getToolByName
log = logging.getLogger(__name__)


def uninstall(context):
    """
    """
    if context.readDataFile('pmb_uninstall.txt') is None:
        return
    for_ = """plone.multilingualbehavior.interfaces.IDexterityTranslatable
        plone.dexterity.interfaces.IEditFinishedEvent"""
    handler_name = "plone.multilingualbehavior.subscriber.handler"

    portal = getSite()
    sm = portal.getSiteManager()
    if not IComponentRegistry.providedBy(sm):
        log.warning('Site manager does not provide component registry')
        return

    handler = _resolveDottedName(handler_name)

    required = []
    for interface in for_.split():
        required.append(_resolveDottedName(interface))

    existing_registration = [(r, n, f, i) for (r, n, f, i) in sm._handler_registrations if (r == tuple(required) and f.__class__ == handler.__class__)]
    # Depending on how often the compentneregistry step had been run in the
    # current site, this list may contain one or many registrations for
    # the same pair of interfaces

    for existing in existing_registration:
        sm.unregisterHandler(
            factory=existing[2], # plone.multilingualbehavior.subscriber.LanguageIndependentModifier
            required=required) # (IDexterityTranslatable, IEditFinishedEvent)
        log.info('Unregistered old event handler')


    # gsm = getGlobalSiteManager()
    # adapter_hook = gsm.adapters.adapter_hook
    # adapters = gsm.utilities._adapters
    # for x in adapters[0]:
    #     for key in adapters[0][x].keys():
    #         if 'plone.multilingualbehavior' in str(key):
    #             del adapters[0][x][key]
    #             log.info("Delete adapter {0} from {1}".format(key, x))
    # gsm.utilities._adapters = adapters

    # provided = gsm.utilities._provided
    # for x in provided:
    #     for interface in interfaces:
    #         if interface in str(x):
    #             del provided[x]
    #             log.info("Delete provided {0} from {1}".format(interface, x))
    # gsm.utilities._provided = provided

    subscribers = sm.adapters._subscribers
    for i, sub in enumerate(subscribers):
        for key in sub.keys():
            if 'multilingualbehavior' in str(key):
                del subscribers[i][key]
    sm.adapters._subscribers = subscribers

    transaction.commit()
    app = portal.restrictedTraverse('/')
    app._p_jar.sync()

    # setup_tool = getToolByName(portal, 'portal_setup')
    # setup_tool.runAllImportStepsFromProfile(
    #     'profile-plone.multilingual:uninstall', purge_old=False)
