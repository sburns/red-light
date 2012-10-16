#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_app.py

Redlight testing
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'


from . import TestCase, app


class ViewTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_index(self):
        "Ensure response on /"
        resp = self.client.get('/')
        self.assert200(resp)

    def test_about(self):
        "Ensure response on /about"
        resp = self.client.get('/about')
        self.assert200(resp)
