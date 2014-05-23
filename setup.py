from setuptools import setup, find_packages
import os

version = '1.2.1'

setup(name='plone.multilingualbehavior',
      version=version,
      description="Dexterity behavior for enabling multilingual extensions",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          ],
      keywords='dexterity multilingual plone',
      author='Plone Foundation',
      author_email='sneridagh@gmail.com',
      url='https://github.com/plone/plone.multilingualbehavior',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.directives.form',
          'plone.directives.dexterity',
          'plone.app.dexterity',
          'plone.multilingual',
          'plone.app.multilingual',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.app.dexterity[relations]',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
