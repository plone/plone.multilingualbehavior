from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent import ObjectModifiedEvent

from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from plone.multilingual.interfaces import ITranslationManager

from plone.multilingualbehavior.interfaces import ILanguageIndependentField

from plone.dexterity import utils

from plone.multilingual.interfaces import ILanguage
from zope.component import queryAdapter

from zope.event import notify
from zope.lifecycleevent import Attributes


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
            translations = self.getAllTranslations(content)
            # Search all Language Independent Fields
            from zope.component import getUtility
            from plone.dexterity.interfaces import IDexterityFTI
            fti = getUtility(IDexterityFTI, name=content.portal_type)
            schema = fti.lookupSchema()
            # For each field modify it at translations
            for field_name in schema:
                if ILanguageIndependentField.providedBy(schema[field_name]):
                    self.modify(translations, field_name, getattr(content, field_name))
            for behavior_schema in \
                   utils.getAdditionalSchemata(content, content.portal_type):
                if behavior_schema is not None:
                    for behavior_field in behavior_schema:
                        if ILanguageIndependentField.providedBy(behavior_schema[behavior_field]):
                            self.modify(translations, behavior_field, getattr(content, behavior_field))
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

    def modify(self, translations, field, value):
        """
        Propagate the value of the language independent field
        for each translation
        """
        for translation in translations:
            setattr(translation, field, value)

handler = LanguageIndependentModifier()
