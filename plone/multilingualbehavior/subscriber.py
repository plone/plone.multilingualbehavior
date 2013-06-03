# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.CMFCore.utils import getToolByName

from plone.multilingual.interfaces import ILanguage
from plone.multilingual.interfaces import ILanguageIndependentFieldsManager
from plone.multilingual.interfaces import ITranslationManager
from plone.multilingualbehavior.interfaces import IDexterityTranslatable
from zope.component import queryAdapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent


class LanguageIndependentModifier(object):
    """Class to handle dexterity editions."""

    stack = []

    def __call__(self, content, event):
        """Called by the event system."""
        if IDexterityTranslatable.providedBy(content):
            if IObjectModifiedEvent.providedBy(event):
                self.handle_modified(content)

    def handle_modified(self, content):
        canonical = ITranslationManager(content).query_canonical()
        if canonical in self.stack:
            return
        else:
            self.stack.append(canonical)

            sm = getSecurityManager()
            acl_users = getToolByName(content, 'acl_users')

            try:
                # Clone the current user and assign a new editor role to
                # allow edition of all translated objects even if the
                # current user whould not have permission to do that.
                tmp_user = UnrestrictedUser(
                    sm.getUser().getId(), '', ['Editor', ], '')

                # Wrap the user in the acquisition context of the portal
                # and finally switch the user to our new editor
                tmp_user = tmp_user.__of__(acl_users)
                newSecurityManager(None, tmp_user)

                # Copy over all language independent fields
                transmanager = ITranslationManager(content)
                fieldmanager = ILanguageIndependentFieldsManager(content)
                for translation in self.get_all_translations(content):
                    trans_obj = transmanager.get_translation(translation)
                    fieldmanager.copy_fields(trans_obj)
                    self.reindex_translation(trans_obj)
            finally:
                # Restore the old security manager
                setSecurityManager(sm)

            self.stack.remove(canonical)

    def reindex_translation(self, translation):
        """Once the modification is done, reindex translation"""
        translation.reindexObject()
        # XXX: Is it really required to fire an ObjectModifiedEvent?
        # fti = getUtility(IDexterityFTI, name=translation.portal_type)
        # schema = fti.lookupSchema()
        # descriptions = Attributes(schema)
        # notify(ObjectModifiedEvent(translation, descriptions))

    def get_all_translations(self, content):
        """Return all translations excluding the just modified content"""
        content_lang = queryAdapter(content, ILanguage).get_language()
        translations = ITranslationManager(content).get_translated_languages()
        translations.remove(content_lang)
        return translations

handler = LanguageIndependentModifier()
