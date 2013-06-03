============================
plone.multilingualbehavior
============================

plone.multilingualbehavior adds multilingual behavior to content types built
with Dexterity. It uses the next generation multilingual engine powered by
five/Zope3 technologies, plone.multilingual.

The behavior provides the Dexterity-driven content with a marker interface
"ITranslatable", and makes available to that translation enabled type all the
translation UI components such as menus, views, etc...

To make your Dexterity content type translatable, add the following line to
the <!-- enabled behaviors --> section in your type's profile::

    <!-- enabled behaviors -->
    <property name="behaviors">
        <element value="plone.multilingualbehavior.interfaces.IDexterityTranslatable" />
    </property>

plone.multilingualbehavior implements language independent fields. The content
of language independent fields is the same across all language versions. This
is convenient, but also a little dangerous, because editing the field on any
language version will change the content on all other language versions.

For details on how to make fields language independent, see the examples in
the test folder. tests/schemata.py shows how to make fields language
independent when using the Grok framework; tests/samplecontent_type.xml shows
how to achieve the same thing in an xml file. It is also possible to set a
field to be language independent through the web, given a sufficiently new
version of plone.schemaeditor.

For more information, please visit:
https://github.com/plone/plone.app.multilingual

Please report any bugs or feature requests to our `issue tracker`_.


Dependencies
------------
- `plone.multilingual`_ (Core and base implementation)
- `plone.app.multilingual`_ (Multilingual configlet, menu and global views)

Contributors
------------

- Ramon Navarro  [bloodbare]  (ramon.nb@gmail.com)
- Víctor Fernández de Alba  [sneridagh]  (sneridagh@gmail.com)
- Daniel Widerin  [saily]


.. _`plone.multilingual`: https://github.com/plone/plone.multilingual
.. _`plone.app.multilingual`: https://github.com/plone/plone.app.multilingual
.. _`issue tracker`: https://github.com/plone/plone.app.multilingual/issues
