#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_api.py

Test Redlight API
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from . import TestCase, URLs, app
import json


class APITest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def get_json(self, url, method, data):
        return json.loads(self.client.post(url, data=data).data)

    def test_filter(self):
        "Ensure a simple API call works as expected"
        json_resp = self.get_json(*URLs['good'])
        for req in ['header', 'err', 'result']:
            self.assertIn(req, json_resp)
        self.assertEqual(len(json_resp['result']), 22)
        output_fields = ['first_name', 'last_name']
        for of in output_fields:
            first_record = json_resp['result'][0]
            self.assertIn(of, first_record)

    def test_no_filter(self):
        "Ensure a filter call with no filter data still works"
        json_resp = self.get_json(*URLs['no_filter'])
        for req in ['header', 'err', 'result']:
            self.assertIn(req, json_resp)
        self.assertEqual(len(json_resp['result']), 50)

    def test_get_columns(self):
        "Test grabbing columns from the API"
        json_resp = self.get_json(*URLs['get_columns'])
        self.assertEqual(0, len(json_resp['err']))
        self.assertTrue('columns' in json_resp)
        self.assertEqual(6, len(json_resp['columns']))

    def test_csv_output(self):
        "Ensure csv output"
        url, _, data = URLs['good_csv']
        raw = self.client.post(path=url, data=data).data
        self.assertIsInstance(raw, basestring)
        splat = raw.splitlines()
        len_header = len(splat[0].split(','))
        # For each line, assert there are as many
        # items within it as header columns
        for l in splat[1:]:
            self.assertEqual(len_header, len(l.split(',')))
