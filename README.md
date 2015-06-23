WheelCMS
========

WheelCMS is a CMS inspired by the functionality offered by Plone (and
other Zope CMS systems) but built on top of Django in stead. If focusses
on content structure in stead of editing webpages.

It offers a nice (bootstrap) interface, themes, creation and WYSIWYG
editing of hierarchical content using content types ("spokes")

One of the goals of WheelCMS is to NOT make the Django admin the CMS admin.
All editing should be done using a clean, userfriendly frontend interface.


INSTALLATION
------------

The easiest way to get started with WheelCMS is to use the sample buildout
project "wheel-site". Simply clone it and run buildout:

    $ git clone git@github.com:wheelcms/wheel-site
      (...)
    $ cd wheel-site
      (...)
    $ virtualenv .
      (...)
    $ bin/pip install zc.buildout
      (...)
    $ bin/buildout -c local.cfg
      (...)
    $ bin/django syncdb

This should give you a fully functional Django project with all dependencies
installed. You can start the application server through bin/django:

    $ bin/django runserver

