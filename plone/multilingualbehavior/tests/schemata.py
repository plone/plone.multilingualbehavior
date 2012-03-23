from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides

from plone.directives import form

from plone.multilingualbehavior import directives
from plone.multilingualbehavior.interfaces import ILanguageIndependentField


class ITestSchemaGrok(form.Schema):
    """Schema used for testing
    """

    title = schema.TextLine(title=u"Title",
                            description=u"Administrative title")

    directives.languageindependent('description')
    description = schema.Text(title=u"Description",
                              required=False)

    directives.languageindependent('description2')
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
