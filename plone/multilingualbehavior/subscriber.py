from zope.component import getUtility
from zope.component import queryAdapter
from zope.event import notify
from zope.lifecycleevent import Attributes
from zope.lifecycleevent import ObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.dexterity.interfaces import IDexterityFTI

from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from plone.multilingual.interfaces import ILanguageIndependentFieldsManager

from plone.multilingual.interfaces import ITranslationManager
from plone.multilingual.interfaces import ILanguage


class LanguageIndependentModifier(object):
    """Class to handle dexterity editions."""

    stack = []

    def __call__(self, content, event):
        """Called by the event system."""
        if IDexterityTranslatable.providedBy(content):
            if IObjectModifiedEvent.providedBy(event):
                self.handleModified(content)

    def handleModified(self, content):
        canonical = ITranslationManager(content).query_canonical()
        if canonical in self.stack:
            return
        else:
            self.stack.append(canonical)

            # Copy over all language independent fields
            translations = self.getAllTranslations(content)
            manager = ILanguageIndependentFieldsManager(content)
            for translation in translations:
                manager.copy_fields(translation)

            fti = getUtility(IDexterityFTI, name=content.portal_type)
            schema = fti.lookupSchema()
            descriptions = Attributes(schema)
            self.reindexTranslations(translations, descriptions)
            self.stack.remove(canonical)

    def reindexTranslations(self, translations, descriptions):
        """Once the modifications are done, reindex all translations"""
        for translation in translations:
            translation.reindexObject()
            notify( ObjectModifiedEvent(translation, descriptions))

    def getAllTranslations(self, content):
        """Return all translations excluding the just modified content"""
        translations_list_to_process = []
        content_lang = queryAdapter(content, ILanguage).get_language()
        canonical = ITranslationManager(content)
        translations = canonical.get_translations()

        for language in translations.keys():
            if language != content_lang:
                translations_list_to_process.append(translations[language])
        return translations_list_to_process

handler = LanguageIndependentModifier()
