# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
from zope import interface
from plone.multilingual.interfaces import ITranslationCloner


class Cloner(object):

    interface.implements(ITranslationCloner)

    def __init__(self, context):
        self.context = context

    def __call__(self, object):
        return
