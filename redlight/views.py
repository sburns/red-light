#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

redsearch view functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import render_template, jsonify, request

from . import app
from . import backend
from .err import RedlightError


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/1/filter.json')
def search():
    err = ''
    results = []
    header = []
    try:
        try:
            api = request.args.get('api', '')
            url = request.args.get('url', '')
            keys = filter(None, request.args.get('keys', '').split(','))
            verbs = filter(None, request.args.get('verbs', '').split(','))
            values = filter(None, request.args.get('values', '').split(','))
            outputs = filter(None, request.args.get('outputs', '').split(','))
            req = [api, url, keys, verbs, values]
            if not all(req):
                # uh oh
                raise ValueError("Bad Argument: %s" % ' '.join(filter(lambda x: not x, req)))
            if not (len(keys) == len(verbs) == len(values)):
                raise Exception("Something strange happened")
            filters = list(zip(keys, verbs, values))
        except Exception as e:
            raise RedlightError("Error parsing parameters (%s)" % e)
        try:
            # pycap call
            db = backend.RCDB(url, api)
        except Exception as e:
            err = "Couldn't connect to REDCap, check your credentials"
        all_keys = list(set(keys + outputs))
        try:
            # pycap call
            db.make_df(all_keys)
        except Exception as e:
            raise RedlightError("Error occured in exporting from REDCap (%s) " % e)
        try:
            # Run the filters, get a new df
            filt_df = db.filter(filters)
            # Merge with filtered
            db.merge(filt_df)
        except Exception as e:
            raise RedlightError("Error occured during filtering and merging (%s)" % e)
        try:
            # Make list of maps
            header = list(outputs)
            header.insert(0, db.index_name())
            results = db.make_outputs(outputs)
        except Exception as e:
            raise RedlightError("Error occured in generating output (%s)" % e)
    except Exception as e:
        err = str(e)
    return jsonify(result=results, header=header, err=err)


@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def inject_filter_verbs():
    return {'verbs': sorted(backend.VERBS.keys())}
