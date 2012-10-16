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
    'good': '/api/1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&keys=test1_score'\
        '&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_url': '/api/1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&keys=test1_score&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_api': '/api/1/filter.json?&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F'\
        '&keys=test1_score&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_keys': '/api/1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F'\
        '&verbs=%3C&values=50&outputs=first_name&outputs=last_name',
    'no_verbs': '/api/1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&keys=test1_score'\
        'values=50&outputs=first_name&outputs=last_name',
    'no_values': '/api/1/filter.json?api=AB5C15042ED4E15BB487C4E15A3AA928'\
        '&url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&keys=test1_score'\
        '&verbs=%3C&outputs=first_name&outputs=last_name',
}