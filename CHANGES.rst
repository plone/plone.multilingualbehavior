Changelog
=========

1.2.2 (2019-12-24)
------------------

- Add uninstall step.
  [bsuttor]

- __name__ method is added for preventing bug when you try to go in Components
  tab into ZMI (/manage_components) or when you try to make a snapshot.
  [bsuttor]

- Add uninstall profile.
  [bsuttor]


1.2.1 (2014-05-23)
------------------

- Use the more specific IEditFinishedEvent rather than IObjectModifiedEvent
  for copying over language independent fields, since IObjectModifiedEvent
  can be thrown multiple times, causing a performace lag [pysailor]

1.2 - 2013-09-24
----------------

- Check property ``bypass_languageindependent_field_permission_check`` exists
  in registry to allow usage with lrf-branch.  [saily]

- Rewrite ``handle_modified`` subscriber to notify ObjectModifiedEvent,
  and pass canonical object as event-description. This replaces the non-working
  semaphore.  Fixes #65
  [saily]

- Switch to a cloned user with a global Editor role to allow synchronization
  of language independant fields of other object (which the current user could
  not have permission to) when modifying an object.  Fixes #66
  [saily]

- We may need to know the language from a object that is not ITranslatable
  [ramon]

1.1 - 2013-06-19
----------------

- Minor PEP8 errors
  [ramon]

1.0 - 2013-04-16
----------------

- Removing ITG usage to ITranslationManager
  [pysailor]
- Added a test for adding multilingual behavior through the web
  [pysailor]


1.0rc1 - 2013-01-26
-------------------

- Adding relationfield to test profile
  [ramon]

- PEP8 cleanup
  [saily]

- Correct import and add new dependency for ``plone.supermodel.model``
  because ``plone.directives.form`` 2.0 does no longer depend on grok.
  [saily]


1.0b3 - 2012-10-04
------------------

- Added tests [sneridagh]
- Cleaning subscribers [ramon]


1.0b2 - 2012-7-9
----------------

- Enable Realtedfields copying the correct translated item when is language independent [ramon]
- Handle case of behaviors where attributes have never been set [do3cc]


1.0b1 - 2012-4-3
----------------

- Schema editor plugin to enable language indepedent fields TTW [ramon]
- Language independent field implementation [ramon]
- Supermodel, grok and native language independent field markers [ramon]
- ILanguage implementation [awello]
