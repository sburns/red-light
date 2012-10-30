#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_backend.py

Testing the redlight backend
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from werkzeug.datastructures import ImmutableMultiDict

from redlight import backend
from redlight.err import RedlightError

from . import TestCase, request, app, URLs, RC_URL, RC_API


class BackendTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_filter_path_v1(self):
        "Assert correct filter URL path"
        url, method, data = URLs['good']
        with app.test_request_context(path=url, data=data, method=method):
            self.assertEqual(request.path, '/v1/filter.json')

    def test_parse_form(self):
        "Test form parsing with good data"
        url, method, data = URLs['good']
        with app.test_request_context(path=url, data=data, method=method):
            api, url, filters = backend.parse_form(request.form)
            self.assertEqual(url, 'https://redcap.vanderbilt.edu/api/')
            self.assertEqual(api, 'AB5C15042ED4E15BB487C4E15A3AA928')
            good_filters = [('test1_score', '<', '50')]
            for f in good_filters:
                self.assertIn(f, filters)

    def test_parse_form_missing_data(self):
        "Test form parsing with missing data"
        regex = 'The %s parameter is required'
        zipped = zip(['no_url', 'no_api', 'no_fields', 'no_verbs', 'no_values'],
            ['url', 'api', 'fields', 'verbs', 'values'])
        for url_key, param in zipped:
            form = ImmutableMultiDict(URLs[url_key][2])
            # self.assertRaises(RedlightError, backend.parse_form, form)
            backend.parse_form(form)
            # with app.test_request_context(path=url, data=data, method=method):
            #     self.assertRaises(RedlightError, backend.parse_form, request)

    def test_get_columns(self):
        "Test grabbing columns from a REDCap"
        correct_columns = ['first_name', 'last_name', 'dob', 'sex',
            'test1_score', 'test2_score']
        comp_columns = backend.get_columns(RC_URL, RC_API)
        self.assertEqual(correct_columns, comp_columns)

    def test_RCDB(self):
        """Ensure we can make an RCDB and the resulting obj has .df"""
        rcdb = backend.RCDB(RC_URL, RC_API, ['first_name', 'last_name'])
        self.assertTrue(hasattr(rcdb, 'df'))
