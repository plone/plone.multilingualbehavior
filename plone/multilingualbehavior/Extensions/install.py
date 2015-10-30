# -*- coding: utf-8 -*-
"""Legacy install/uninstall-methods to guard from re-installing/uninstalling"""
from Products.CMFCore.utils import getToolByName


def uninstall(context, reinstall=False):
    if not reinstall:
        setup_tool = getToolByName(context, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(
            'profile-plone.multilingualbehavior:uninstall', purge_old=False)