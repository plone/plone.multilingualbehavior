import martian

from zope.interface import Interface
from zope.interface.interface import TAGGED_DATA
from zope.interface.interfaces import IInterface

from plone.supermodel.interfaces import FILENAME_KEY, SCHEMA_NAME_KEY, FIELDSETS_KEY
from plone.supermodel.model import Fieldset

from plone.autoform.interfaces import OMITTED_KEY, WIDGETS_KEY, MODES_KEY, ORDER_KEY
from plone.autoform.interfaces import READ_PERMISSIONS_KEY, WRITE_PERMISSIONS_KEY

TEMP_KEY = '__form_directive_values__'

# Storages

class LanguageIndependentStorage(object):
    """Stores the primary() directive value in a schema tagged value.
    """

    def set(self, locals_, directive, value):
        tags = locals_.setdefault(TAGGED_DATA, {})
        tags.setdefault(directive.dotted_name(), []).extend(value)

    def get(self, directive, component, default):
        return component.queryTaggedValue(directive.dotted_name(), default)

    def setattr(self, context, directive, value):
        context.setTaggedValue(directive.dotted_name(), value)

# Directives

class languageindependent(martian.Directive):
    """Directive used to mark one or more fields as 'languageindependent'
    """
    
    scope = martian.CLASS
    store = LanguageIndependentStorage()
    
    def factory(self, *args):
        return args

__all__ = ('languageindependent',)
