#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Redlight, a web app for quick ad-hoc searches against redcap projects
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'
__version__ = '1.0.2'

from flask import Flask

app = Flask(__name__)

from . import views
