from zope.interface import Interface
from zope import schema
from plone.directives import form

from plone.multilingualbehavior.interfaces import MULTILINGUAL_KEY

class ITestSchema(form.Schema):
    """Schema used for testing
    """
    
    title = schema.TextLine(title=u"Title",
                            description=u"Administrative title")
                        
    description = schema.Text(title=u"Description",
                              required=False)

ITestSchema.setTaggedValue(MULTILINGUAL_KEY, {'title':False,'description':True})

