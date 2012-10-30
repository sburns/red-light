#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Common things for testing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask.ext.testing import TestCase
from flask import request
from redlight import app

RC_URL = 'https://redcap.vanderbilt.edu/api/'
RC_API = 'AB5C15042ED4E15BB487C4E15A3AA928'


URLs = {
    'good': ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
                'url': 'https://redcap.vanderbilt.edu/api/', 'fields': 'test1_score',
                'verbs': '<', 'values': '50', 'outputs': ['first_name', 'last_name']}),
    'good_csv':  ('/v1/filter.csv', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
             'url': 'https://redcap.vanderbilt.edu/api/', 'fields': 'test1_score',
             'verbs': '<', 'values': '50', 'outputs': ['first_name', 'last_name']}),
    'no_url':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'fields': 'test1_score', 'verbs': '<', 'values': '50',
            'outputs': ['first_name', 'last_name']}),
    'no_api':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/', 'fields': 'test1_score',
            'verbs': '<', 'values': '50', 'outputs': ['first_name', 'last_name']}),
    'no_fields':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/', 'verbs': '<', 'values': '50',
            'outputs': ['first_name', 'last_name']}),
    'no_verbs':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/', 'fields': 'test1_score',
            'values': '50', 'outputs': ['first_name', 'last_name']}),
    'no_values':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/', 'fields': 'test1_score',
            'verbs': '<', 'outputs': ['first_name', 'last_name']}),
    'no_filter':  ('/v1/filter.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/'}),
    'get_columns':  ('/v1/columns.json', 'POST', {'api': 'AB5C15042ED4E15BB487C4E15A3AA928',
            'url': 'https://redcap.vanderbilt.edu/api/'})
}
