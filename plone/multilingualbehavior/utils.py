# -*- coding: utf-8 -*-
from zope import interface
from zope.component import getUtility

from plone.dexterity import utils
from plone.dexterity.interfaces import IDexterityFTI

from plone.multilingual.interfaces import ILanguageIndependentFieldsManager

from plone.multilingualbehavior.interfaces import ILanguageIndependentField

class LanguageIndependentFieldsManager(object):
    interface.implements(ILanguageIndependentFieldsManager)

    def __init__(self, context):
        self.context = context

    def copy_fields(self, translation):
        fti = getUtility(IDexterityFTI, name=self.context.portal_type)
        schemas = []
        schemas.append(fti.lookupSchema())

        for behavior_schema in \
                utils.getAdditionalSchemata(self.context, self.context.portal_type):
            if behavior_schema is not None:
                schemas.append(behavior_schema)

        for schema in schemas:
            for field_name in schema:
                if ILanguageIndependentField.providedBy(schema[field_name]):
                    value = getattr(self.context, field_name)
                    setattr(translation, field_name, value)



