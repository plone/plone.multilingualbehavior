#
# Convenience API
#

import zope.deferredimport
import schemaeditor

zope.deferredimport.defineFrom('plone.multilingualbehavior.schema',
    'languageindependent',
)