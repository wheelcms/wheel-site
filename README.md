WheelCMS
========

WheelCMS is a CMS inspired by the functionality offered by Plone (and
other Zope CMS systems) but built on top of Django in stead.

It offers a nice (bootstrap) interface, themes, creation and WYSIWYG
editing of hierarchical content using content types ("spokes")


INSTALLATION
------------

The easiest way to get started with WheelCMS is to use the sample buildout
project "wheel-cms". Simply clone it and run buildout:

    $ git clone git@github.com:wheelcms/wheel-cms
      (...)
    $ cd wheel-cms
      (...)
    $ virtualenv .
      (...)
    $ bin/pip install zc.buildout
      (...)
    $ bin/buildout
      (...)
    $ bin/django syncdb

This should give you a fully functional Django project with all dependencies
installed. You can start the application server through bin/django:

    $ bin/django runserver

