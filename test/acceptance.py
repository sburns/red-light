#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" acceptance.py

Acceptance testing for Red-Light
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2012 Vanderbilt University. All Rights Reserved'

from time import time, sleep
from splinter import Browser
import requests
from urlparse import urljoin

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


def test_api(url):
    print "Testing API..."
    data = dict(url=RCURL, api=RCAPI, fields='test1_score', verbs='>',
        values='50', outputs='first_name')

    def response_from_post(url):
        # use the same data
        print "Posting to %s..." % url
        return requests.post(url, data=data)

    def test_endpoint(url, endpoint, required):
        success = False
        print "Testing %s..." % endpoint
        json = response_from_post(urljoin(url, endpoint)).json
        success = all(map(lambda x: x in json, required))
        if success:
            print "%s passed." % endpoint
        return success

    return all([test_endpoint(url, '/v1/columns.json', ['err', 'columns']),
                test_endpoint(url, '/v1/filter.json', ['header', 'result', 'err'])])


def test_ui(url, browser):
    print "Testing UI..."
    success = False
    with Browser(browser) as b:
        b.visit(url)
        inputURL = b.find_by_id('inputURL')[0]
        inputAPI = b.find_by_id('inputAPI')[0]
        inputURL.fill(RCURL)
        inputAPI.fill(RCAPI)

        value1 = b.find_by_id('value1')[0]
        value1.click()
        # Remove focus from API, wait for get_columns
        sleep(2)
        credentialCheck = b.find_by_id('credentialCheck')[0]
        assert "REDCap access successful" == credentialCheck.text
        print "Column grabbing success"

        field1 = b.find_by_id('field1')[0]
        verb1 = b.find_by_id('select1')[0]

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

        while 'Searching' in msg.text:
            if time() > tend:
                print "Filtering failed"
                break
        else:
            assert '28 records' in msg.text
            print "Filtering success"
            success = True
    return success

if __name__ == '__main__':
    args = parse_args()
    url, browser = args.url, args.browser
    if not test_ui(url, browser):
        print "Failed UI test"
    else:
        print "Passed UI test"
    print
    print
    if not test_api(url):
        print "Failed API test"
    else:
        print "Passed API test"
