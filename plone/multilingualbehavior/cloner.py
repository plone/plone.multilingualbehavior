# -*- coding: utf-8 -*-
from zope import interface
from zope.component import getUtility

from plone.dexterity import utils
from plone.dexterity.interfaces import IDexterityFTI
from plone.multilingual.interfaces import ITranslationCloner
from plone.multilingualbehavior.interfaces import ILanguageIndependentField

class Cloner(object):

    interface.implements(ITranslationCloner)

    def __init__(self, context):
        self.context = context

    def __call__(self, obj):
        fti = getUtility(IDexterityFTI, name=obj.portal_type)
        schemas = []
        schemas.append(fti.lookupSchema())

        for behavior_schema in \
                utils.getAdditionalSchemata(self.context, obj.portal_type):
            if behavior_schema is not None:
                schemas.append(behavior_schema)

        for schema in schemas:
            for field_name in schema:
                if ILanguageIndependentField.providedBy(schema[field_name]):
                    value = getattr(self.context, field_name)
                    setattr(obj, field_name, value)
