#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" acceptance.py

Acceptance testing for Red-Light
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

import sys
from time import time
from splinter import Browser

RCURL, RCAPI = ('https://redcap.vanderbilt.edu/api/', 'AB5C15042ED4E15BB487C4E15A3AA928')


def parse_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Run acceptance tests on Red-Light")
    def_browser = 'chrome'
    parser.add_argument('--browser', default=def_browser,
        help="Select browser to use [default: %s]" % def_browser)
    def_url = 'http://127.0.0.1:5000'
    parser.add_argument('--url', default=def_url,
        help="Url to test against [default: %s]" % def_url)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    browser_driver = args.browser
    testing_url = args.url
    with Browser(browser_driver) as b:
        b.visit(testing_url)
        inputURL = b.find_by_id('inputURL')[0]
        inputAPI = b.find_by_id('inputAPI')[0]
        inputURL.fill(RCURL)
        inputAPI.fill(RCAPI)

        field1 = b.find_by_id('field1')[0]
        verb1 = b.find_by_id('select1')[0]
        value1 = b.find_by_id('value1')[0]

        field1.fill('test1_score')
        verb1.type('>')
        value1.fill('50')

        output1 = b.find_by_id('col1')[0]
        output1.fill('first_name')

        filter_search_btn = b.find_by_id('filter')[0]
        filter_search_btn.click()

        TO = 5  # sec
        tend = time() + TO
        msg = b.find_by_id('resultText')[0]

        success = False
        while 'Searching' in msg.text:
            if time() > tend:
                print "Filtering failed"
                ec = 1
                break
        else:
            assert '28 records' in msg.text
            print "Filtering success"
            ec = 0
    sys.exit(ec)
