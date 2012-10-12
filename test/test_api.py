#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_api.py

Test Redlight API
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask.ext.testing import TestCase

from redlight import app


class ViewTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_filterjson(self):
        "Ensure a simple API call works as expected"
        response = self.client.get('/api/1/filter.json?url=https%3A%2F%2Fredcap.vanderbilt.edu%2Fapi%2F&api=AB5C15042ED4E15BB487C4E15A3AA928&keys=test1_score&verbs=%3C&values=50&outputs=first_name%2Clast_name')
        for req in ['header', 'err', 'result']:
            self.assertIn(req, response.json)
        self.assertEqual(len(response.json['result']), 22)
