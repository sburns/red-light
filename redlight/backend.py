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


class DB(object):
    """Base"""

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

    def make_outputs(self, keys):
        # Remove columns that aren't in keys
        all_results = []
        from_df = self.df.to_dict()
        for record in self.df.index:
            record_dict = {}
            record_dict[self.df.index.name] = str(record)
            for key in keys:
                if key in from_df:
                    record_dict[key] = from_df[key][record]
            all_results.append(record_dict)
        return all_results

    def index_name(self):
        return self.df.index.name


class RCDB(DB):
    """Class representing a redcap database"""

    def __init__(self, url, api):
        self.proj = Project(url, api)

    def make_df(self, fields):
        csv = StringIO(self.proj.export_records(fields=fields, format='csv'))
        self.df = pd.read_csv(csv, index_col=self.proj.def_field)
