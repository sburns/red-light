#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_backend.py

Testing the redlight backend
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from . import TestCase, request, app, URLs

from redlight import backend, err


class ViewTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_filter_path_v1(self):
        "Assert correct filter URL path"
        with app.test_request_context(URLs['good']):
            self.assertEqual(request.path, '/v1/filter.json')

    def test_parse_args(self):
        "Test argument parsing with good params"
        with app.test_request_context(URLs['good']):
            api, url, filters = backend.parse_arguments(request)
            self.assertEqual(url, 'https://redcap.vanderbilt.edu/api/')
            self.assertEqual(api, 'AB5C15042ED4E15BB487C4E15A3AA928')
            good_filters = [('test1_score', '<', '50')]
            for f in good_filters:
                self.assertIn(f, filters)

    def test_parse_args_bad_params(self):
        "Test argument parsing with bad params"
        # No url
        zipped = zip(['no_url', 'no_api', 'no_fields', 'no_verbs', 'no_values'],
            ['url', 'api', 'fields', 'verbs', 'values'])
        for url_key, param in zipped:
            with app.test_request_context(URLs[url_key]):
                regex = 'The %s parameter is required' % param
                with self.assertRaisesRegexp(err.RedlightError, regex):
                    api, url, filters = backend.parse_arguments(request)
