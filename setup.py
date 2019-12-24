from setuptools import setup, find_packages

version = '1.2.2'

setup(name='plone.multilingualbehavior',
      version=version,
      description="Dexterity behavior for enabling multilingual extensions",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.rst").read(),
      # Get more strings from https://pypi.org/classifiers/
      classifiers=[
          "Development Status :: 7 - Inactive",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
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
