from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish

from plone.dexterity.interfaces import IDexterityFTI

from plone.multilingualbehavior.interfaces import IDexterityTranslatable


class AddTranslationViewTraverser(object):

    """Add view traverser.
    """

    adapts(IFolderish, Interface)
    implements(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):
        import pdb; pdb.set_trace()
        (type_obj, tg) = name.split('++')
        ttool = getToolByName(self.context, 'portal_types')
        ti = ttool.getTypeInfo(type_obj)
        if not IDexterityFTI.providedBy(ti):
            # we are not on DX content
            return
        # set the self.context to the place where it should be stored
        if not IFolderish.providedBy(self.context):
            self.context = self.context.__parent__
        if ti is not None:
            add_view = queryMultiAdapter((self.context, self.request, ti),
                                         name=ti.factory)
            if add_view is None:
                add_view = queryMultiAdapter((self.context, self.request, ti))
            if add_view is not None:
                add_view.__name__ = ti.factory
                view_to_send = add_view.__of__(self.context)
                view_to_send.tg = tg
                return view_to_send

        raise TraversalError(self.context, name)
