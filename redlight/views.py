#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" views.py

red-light view functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from flask import render_template, jsonify, request

from . import __version__ as version
from . import app
from . import backend
from .err import RedlightError


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/v1/columns.<format>')
def get_columns(format):
    err = ''
    columns = []
    try:
        api, url, _ = backend.parse_arguments(request, req_filter=False)
        columns = backend.get_columns(url, api)
    except Exception as e:
        err = "Error:%s" % str(e)
    finally:
        return jsonify(err=err, columns=columns)


@app.route('/v1/filter.<format>')
def search(format):
    err = ''
    try:
        try:
            outputs = filter(None, request.args.getlist('outputs'))
            api, url, filters = backend.parse_arguments(request)
        except Exception as e:
            raise RedlightError("Error occured parsing arguments (%s)" % e)
        keys = [f[0] for f in filters]
        all_keys = list(set(keys + outputs))
        try:
            # pycap calls
            db = backend.RCDB(url, api, all_keys)
        except Exception as e:
            err = "Couldn't connect to or export from REDCap, check your credentials"
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
            results = db.make_outputs(outputs, format=format)
        except Exception as e:
            raise RedlightError("Error occured in generating output (%s)" % e)
    except Exception as e:
        err = str(e)
        results = []
        header = []
    if format == 'json':
        return jsonify(result=results, header=header, err=err)
    else:
        return err + results


@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def inject_filter_verbs():
    return {'verbs': sorted(backend.VERBS.keys())}


@app.context_processor
def inject_version():
    return {'version': version}
