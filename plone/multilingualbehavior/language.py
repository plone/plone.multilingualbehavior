from zope import interface
from zope.component.hooks import getSite

from plone.directives import form
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.metadata import ICategorization

from plone.multilingual.interfaces import LANGUAGE_INDEPENDENT
from plone.multilingual.interfaces import ILanguage


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


# make sure the add form shows the default creator
# this should go to p.a.dexterity in the future
@form.default_value(field=ICategorization['language'])
def setDefaultLanguage(data):
    portal = getSite()
    pl = getToolByName(portal, "portal_languages")
    return pl.getPreferredLanguage()

ICategorization['language'].readonly = True