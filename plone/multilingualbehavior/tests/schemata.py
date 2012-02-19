from zope.interface import Interface
from zope import schema
from plone.directives import form
from plone.multilingualbehavior import schema as multilingual_form

from plone.multilingualbehavior.interfaces import MULTILINGUAL_KEY
from plone.multilingualbehavior.interfaces import ILanguageIndependentField
from zope.interface import implements, alsoProvides


class ITestSchemaGrok(form.Schema):
    """Schema used for testing
    """

    title = schema.TextLine(title=u"Title",
                            description=u"Administrative title")

    multilingual_form.languageindependent('description')
    description = schema.Text(title=u"Description",
                              required=False)

    multilingual_form.languageindependent('description2')
    description2 = schema.Text(title=u"Description 2",
                              required=False)


class ITestSchemaInterface(Interface):
    """Schema used for testing
    """

    title = schema.TextLine(title=u"Title",
                            description=u"Administrative title")

    description = schema.Text(title=u"Description",
                              required=False)

alsoProvides(ITestSchemaInterface['description'],ILanguageIndependentField)