#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 Paul Michael Furley <paul@paulfurley.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Vodafone Scraper

Usage:
  vodafone-scraper show  [--verbose]
  vodafone-scraper alert [--minutes=<minutes>] [--texts=<texts>]
                         [--megabytes=<megabytes>]

Options:
  -h --help                      Show this help.
  --verbose                      Show debug output.

  --auth=<username>:<password>   Vodafone username/password. If not supplied,
                                 the environment variables VODAFONE_USERNAME
                                 and VODAFONE_PASSWORD are used.

  --minutes=<minutes>            Warn if minutes >= minutes
  --texts=<texts>                Warn if minutes >= texts
  --megabytes=<megabytes>        Warn if megabytes >= megabytes
"""

import contextlib
import logging
import os
import sys

from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import selenium.webdriver.support.ui as ui
from docopt import docopt
import lxml.html


LOGIN_URL = 'https://www.vodafone.co.uk/myvodafone/faces/home'


def main():
    options = docopt(__doc__, version='1.0.1')
    if options['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    username, password = get_username_password(options)

    if not username or not password:
        print("No username/password supplied. Either pass on the command line "
              "or set VODAFONE_USERNAME and VODAFONE_PASSWORD in your "
              "environment.")
        return 1

    usage = get_usage(username, password)
    display_output(options, usage)
    return 0


def display_output(options, usage):
    """
    Actually output to screen the result of the command. In 'show' mode this is
    simply the current usage. In 'alert' mode we only output if one of the
    usage criteria is above the given threshold.
    """
    if options['show']:
        for key, value in usage.items():
            print("{}: {}".format(key, value))

    elif options['alert']:
        print_alerts(options, usage)


def get_usage(username, password):
    html = get_summary_page_html(username, password)
    return parse_usage(html)


def get_username_password(options):
    """
    Parse the username/password from the command line or environment.
    """
    if '--auth' in options:
        username, password = options['--auth'].split(':')
    else:
        username = os.environ.get('VODAFONE_USERNAME')
        password = os.environ.get('VODAFONE_PASSWORD')
    return username, password


def print_alerts(options, usage):
    """
    Generate warning messages to screen depending on usage & thesholds.

    >>> print_alerts({'--minutes': '100'}, {'minutes': 150})
    ALERT: 150 minutes used.
    """
    #print("options: {}\nusage: {}".format(options, usage))
    for metric in ('minutes', 'texts', 'megabytes'):
        alert_level = options.get('--{}'.format(metric))

        if alert_level is not None:
            if usage[metric] >= int(alert_level):
                print("ALERT: {0} {1} used.".format(usage['minutes'], metric))


def get_summary_page_html(username, password):
    """
    Use the Selenium webdriver to log into the Vodafone site and return the
    HTML of the front page, after it's finished rendering the summary usage
    in Javascript.
    """
    with contextlib.closing(webdriver.Firefox(custom_firefox_profile(
            images=False, css=True, flash=False))) as driver:
        driver.get(LOGIN_URL)
        wait = ui.WebDriverWait(driver, 120)
        wait.until(lambda driver: 'log into My Vodafone' in driver.title)
        assert "log into My Vodafone" in driver.title
        username_box = driver.find_element_by_name('username')
        password_box = driver.find_element_by_name('password')
        submit_button = driver.find_element_by_xpath("//input[@type='submit']")

        username_box.send_keys(username)
        password_box.send_keys(password)
        submit_button.click()

        wait.until(lambda driver: driver.find_element_by_xpath(
            "//div[@class='specialCharges']"))
        logging.debug("Page has finished loading.")
        html = driver.page_source
    return html


def custom_firefox_profile(images=False, css=False, flash=False):
    """
    Create a new Firefox profile with some custom configuration.
    """
    profile = FirefoxProfile()
    if not css:
        profile.set_preference('permissions.default.stylesheet', 2)
    if not images:
        profile.set_preference('permissions.default.image', 2)
    if not flash:
        profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    return profile


def parse_usage(html):
    """
    Extract the usage integers out of the summary HTML and return them as a
    dictionary with keys 'minutes', 'texts', 'megabytes'.
    """
    with open('test.html', 'w') as f:
        f.write(html.encode('utf-8'))
    lxml_root = lxml.html.fromstring(html)
    fields = OrderedDict([
        ('minutes', ("//*[contains(text(), 'minutes used')]/"
                     "preceding-sibling::strong/text()", int)),

        ('texts', ("//*[contains(text(), 'texts used')]/"
                   "preceding-sibling::strong/text()", int)),

        ('megabytes', ("//*[contains(text(), 'MB data used')]/"
                       "preceding-sibling::strong/text()", int)),
    ])
    data = {}
    for field, (xpath, convert_function) in fields.items():
        logging.debug(xpath)
        matching_elements = lxml_root.xpath(xpath)
        assert len(matching_elements) == 1
        value = matching_elements[0]

        if convert_function:
            value = convert_function(value)
        data[field] = value
    return data


if __name__ == '__main__':
    sys.exit(main())
