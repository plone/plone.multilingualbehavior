from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from plone.multilingual.interfaces import ITranslationManager

from plone.multilingualbehavior.interfaces import ILanguageIndependentField

from plone.dexterity import utils

from plone.multilingual.interfaces import ILanguage
from zope.component import queryAdapter


class LanguageIndependentModifier(object):
    """Class to handle dexterity editions."""

    stack = []

    def __call__(self, content, event):
        """Called by the event system."""
        if IDexterityTranslatable.providedBy(content):
            if IObjectAddedEvent.providedBy(event):
                self.handleAdded(content)
            elif IObjectModifiedEvent.providedBy(event):
                self.handleModified(content)
            elif IObjectRemovedEvent.providedBy(event):
                self.handleRemoved(content)

    def handleAdded(self, object):
        translations = self.getAllTranslations(object)
        self.modify(translations, None)

    def handleModified(self, content):
        canonical = ITranslationManager(content)
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

            self.reindexTranslations(translations)
            self.stack.remove(canonical)

    def handleRemoved(self, object):
        canonical = ITranslationManager(object)
        if canonical in self.pile_of_translations_of_modified:
            return
        else:
            self.stack.append(canonical)
            translations = self.getAllTranslations(object)
            self.modify(translations, None)
            self.stack.pop(canonical)

    def reindexTranslations(self, translations):
        """Once the modifications are done, reindex all translations"""
        for translation in translations:
            translation.reindexObject()

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
