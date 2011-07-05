from plone.multilingual.interfaces import (
    ILanguage,
)
from zope import interface
from plone.multilingual.interfaces import LANGUAGE_INDEPENDENT


class Language(object):

    def __init__(self, context):
        self.context = context

    interface.implements(ILanguage)

    def get_language(self):
        language = self.context.language
        if not language:
            language = LANGUAGE_INDEPENDENT
        return language

    def set_language(self, language):
        self.context.language = language
