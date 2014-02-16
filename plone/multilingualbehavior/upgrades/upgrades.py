# -*- coding: utf-8 -*-
from Products.GenericSetup.utils import _resolveDottedName
from zope.component.hooks import getSite
from zope.component.interfaces import IComponentRegistry

import logging
log = logging.getLogger(__name__)


def enable_ieditfinishedevent(context):
    """
        Replaces handler registration for IObjectModifiedEvent with
        IEditFinishedEvent.
        The important part of this step is purging the component registry of
        old registrations for adapters. Due to the way unregistering works in
        the registry (by comparing actual factory instances instead of
        classes), we cannot rely on the registry to perform this task.
    """
    old_for_ = """plone.multilingualbehavior.interfaces.IDexterityTranslatable
        zope.lifecycleevent.interfaces.IObjectModifiedEvent"""
    new_for_ = """plone.multilingualbehavior.interfaces.IDexterityTranslatable
        plone.dexterity.interfaces.IEditFinishedEvent"""
    handler_name = "plone.multilingualbehavior.subscriber.handler"
    portal = getSite()
    sm = portal.getSiteManager()
    if not IComponentRegistry.providedBy(sm):
        log.warning('Site manager does not provide component registry')
        return

    handler = _resolveDottedName(handler_name)
    required_old = []
    for interface in old_for_.split():
        required_old.append(_resolveDottedName(interface))

    required_new = []
    for interface in new_for_.split():
        required_new.append(_resolveDottedName(interface))

    # Very similar code is found in zope.component.registry.Components,
    # method unregisterHandler()
    # But here we compare the __class__ of each factory, not the factory
    # itself
    existing_registration = [
        (r, n, f, i)
        for (r, n, f, i)
        in sm._handler_registrations
        if (r == tuple(required_old) and f.__class__ == handler.__class__)
    ]

    # Depending on how often the compentneregistry step had been run in the
    # current site, this list may contain one or many registrations for
    # the same pair of interfaces
    for existing in existing_registration:
        if sm.unregisterHandler(
                factory=existing[2], required=required_old):
            log.info('Unregistered old event handler')

    sm.registerHandler(handler, required=required_new)
