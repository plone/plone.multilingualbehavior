import martian
from martian.error import GrokImportError

from zope.interface import alsoProvides

from plone.multilingualbehavior.interfaces import ILanguageIndependentField
from plone.multilingualbehavior.directives import languageindependent
from plone.directives.form.schema import Schema

class MultilingualGrokker(martian.InstanceGrokker):
    martian.component(Schema.__class__)
    martian.directive(languageindependent)

    def execute(self, interface, config, **kw):

        languageindependentfields = interface.queryTaggedValue(languageindependent.dotted_name(), [])
        for fieldName in languageindependentfields:
            try:
                alsoProvides(interface[fieldName], ILanguageIndependentField)
            except KeyError:
                raise GrokImportError("Field %s set in languageindependent() directive on %s not found" % (fieldName, interface,))
        return True
