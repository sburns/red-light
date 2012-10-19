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

URLs = {
    'good': '/v1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&fields=test1_score'\
        '&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'good_csv': '/v1/filter.csv?api=AB5C15042ED4E15BB487C4E15A3AA928&'\
        'url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&fields=test1_score&'\
        'verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_url': '/v1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&fields=test1_score&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_api': '/v1/filter.json?&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F'\
        '&fields=test1_score&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_fields': '/v1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F'\
        '&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_verbs': '/v1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&fields=test1_score'\
        'values=50&outputs=first_name&outputs=last_name',
    'no_values': '/v1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&fields=test1_score'\
        '&verbs=%3C&outputs=first_name&outputs=last_name',
}