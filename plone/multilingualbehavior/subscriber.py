from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from plone.multilingual.interfaces import ITranslationManager

class LanguageIndependentModifier:
    """Class to handle dexterity editions."""

    stack = []

    def __call__(self, event):
        """Called by the event system."""
        if IDexterityTranslatable.providedBy(event.object):
            if IObjectAddedEvent.providedBy(event):
                self.handleAdded(event.object)
            elif IObjectModifiedEvent.providedBy(event):
                self.handleModified(event.object)
            elif IObjectRemovedEvent.providedBy(event):
                self.handleRemoved(event.object)

    def handleAdded(self, object):
        translations = self.getAllTranslations(object)
        self.modify(translations, None)

    def handleModified(self, object):
        canonical = ITranslationManager(object)
        if canonical in self.stack:
            return
        else:
            self.stack.append(canonical)
            translations = self.getAllTranslations(object)
            # Search all Language Independent Fields
            # For each modify it at translations
            self.modify(translations, None)
            self.stack.pop(canonical)

    def handleRemoved(self, object):
        canonical = ITranslationManager(object)
        if canonical in self.pile_of_translations_of_modified:
            return
        else:
            self.stack.append(canonical)
            translations = self.getAllTranslations(object)
            self.modify(translations, None)
            self.stack.pop(canonical)

    def getAllTranslations(self, object):
        """Return all translations"""
        canonical = ITranslationManager(object)
        translations = canonical.get_translations()
        return translations

    def modify(self, translations, field):
        """Edit the language independent field"""
        # TODO
        pass
  
handler = LanguageIndependentModifier()
