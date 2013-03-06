#!/usr/bin/env python2.7

import sys
import os

PROJECT=os.environ['PROJECT']

base = os.path.dirname(__file__) 
execfile(os.path.join(base, "bin/django"), {})

# os.environ['DJANGO_SETTINGS_MODULE'] = 

sys.path[0:0] = [
    os.path.join(base),
    os.path.join(base, PROJECT),
    os.path.join(base, 'lib/python2.7/site-packages')
]

import django.core.handlers.wsgi 
application = django.core.handlers.wsgi.WSGIHandler()
