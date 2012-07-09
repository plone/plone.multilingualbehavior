from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides

from plone.directives import form

from plone.multilingualbehavior import directives
from plone.multilingualbehavior.interfaces import ILanguageIndependentField

from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree import ObjPathSourceBinder


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


class IRelatedTestSchemaGrok(form.Schema):
    """Schema used for related testing
    """

    directives.languageindependent('multiple')
    multiple = RelationList(title=u"Multiple (Relations field)",
                           required=False,
                           value_type=RelationChoice(title=u"Multiple",
                     vocabulary="plone.formwidget.relations.cmfcontentsearch"))

    directives.languageindependent('single')
    single = RelationChoice(title=u"Single",
                       required=False,
                       source=ObjPathSourceBinder(object_provides=ITestSchemaGrok.__identifier__))


class ITestSchemaInterface(Interface):
    """Schema used for testing
    """

    title = schema.TextLine(title=u"Title",
                            description=u"Administrative title")

    description = schema.Text(title=u"Description",
                              required=False)


alsoProvides(ITestSchemaInterface['description'], ILanguageIndependentField)

