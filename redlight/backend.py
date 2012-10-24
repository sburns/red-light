#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" backend.py

Backend redcap connection/filtering functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

import operator as op

from StringIO import StringIO
import pandas as pd
from redcap import Project
from numpy import dtype
from flask import request

from .err import RedlightError

VERBS = {
    "<": op.lt,
    ">": op.gt,
    "=": op.eq,
    "<=": op.le,
    ">=": op.ge,
}

DTYPE_COERCER = {dtype('float64'): float,
                 dtype('int64'): int,
                 dtype('object'): str}


def parse_arguments(req, req_filter=True):
    api = request.args.get('api')
    url = request.args.get('url')
    fields = request.args.getlist('fields')
    verbs = request.args.getlist('verbs')
    values = request.args.getlist('values')
    if req_filter:
        required = zip(['api', 'url', 'fields', 'verbs', 'values'],
                     [api, url, fields, verbs, values])
    else:
        required = zip(['api', 'url'], [api, url])
    for param, val in required:
        if not val:
            raise RedlightError("The %s parameter is required" % param)
    if not (len(fields) == len(verbs) == len(values)):
        raise RedlightError("fields, verbs and values must be the same length")
    filters = list(zip(fields, verbs, values))
    return api, url, filters


def get_columns(url, api):
    p = Project(url, api)
    return p.field_names


class DB(object):
    """Base
    Subclasses need to make self.df in contstructor"""

    def __init__(self):
        raise NotImplementedError

    def make_df(self):
        raise NotImplementedError

    def merge(self, right_df):
        """ Just reindex based on the incoming df"""
        self.df = self.df.reindex(right_df.index)

    def filter(self, filters):
        results = self.df.copy()
        # Build constraints and iteratively apply
        for key, verb, value in filters:
            dtype = self.df[key].dtype
            coerce_value = DTYPE_COERCER[dtype](value)
            c = results[key].map(lambda x: VERBS[verb](x, coerce_value))
            results = results[c]
        return results

    def make_outputs(self, keys, format='json'):
        # Remove columns that aren't in keys (but were used to filter)
        cols_not_needed = set(self.df.columns) - set(keys)
        map(self.df.pop, cols_not_needed)
        if format == 'json':
            all_results = []
            from_df = self.df.to_dict()
            for record in self.df.index:
                record_dict = {}
                record_dict[self.df.index.name] = str(record)
                for key in keys:
                    if key in from_df:
                        # dtypes used in pandas aren't json-able, so coerce them to
                        # normal python types
                        coercer = DTYPE_COERCER[self.df[key].dtype]
                        record_dict[key] = coercer(from_df[key][record])
                all_results.append(record_dict)
        elif format == 'csv':
            result_buf = StringIO()
            self.df.to_csv(result_buf)
            all_results = result_buf.getvalue()
        elif format == 'html':
            all_results = self.df.to_html()
        return all_results

    def index_name(self):
        return self.df.index.name


class RCDB(DB):
    """Class representing a redcap database"""

    def __init__(self, url, api, initial_fields):
        self.proj = Project(url, api)
        self.make_df(initial_fields)

    def make_df(self, fields):
        csv = StringIO(self.proj.export_records(fields=fields, format='csv'))
        self.df = pd.read_csv(csv, index_col=self.proj.def_field)
