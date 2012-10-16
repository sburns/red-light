#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_api.py

Test Redlight API
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from . import TestCase, URLs, app


class ViewTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_filter(self):
        "Ensure a simple API call works as expected"
        response = self.client.get(URLs['good'])
        for req in ['header', 'err', 'result']:
            self.assertIn(req, response.json)
        self.assertEqual(len(response.json['result']), 22)
        output_fields = ['first_name', 'last_name']
        for of in output_fields:
            first_record = response.json['result'][0]
            self.assertIn(of, first_record)
