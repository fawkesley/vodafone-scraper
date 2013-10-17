# Overview

**vodafone-scraper** is a command-line utility to get your current usage (ie
minutes, texts, data & extra spending) from your UK Vodafone *MyAccount*
online service.

It uses Selenium browser automation. If you can work out how to authenticate
reliably without using a complete browser, pull requests are very welcome :)

# Installation

The python library ``lxml`` requires ``libxml2-dev`` and ``libxslt1-dev`` to
build inside a virtualenv. On debian-like systems these can be installed like
this:

```
$ sudo apt-get install libxml2-dev libxslt1-dev
```

Install the utility using pip, either to your system:

```
sudo pip install scrape-vodafone
```

Or in your home directory (.local):

```
pip install --user scrape-vodafone
```

Note that you must ensure that ``~/.local/bin`` is in your ``$PATH`` variable
if you install as a local user. You can do this by adding the following line to
your ``~/.bashrc`` file:

```
export PATH=$PATH:~/.local/bin
```

# Usage

To get started, run the tool with your username/email and password:

```
$ vodafone-scraper show "--auth=me@myemail.com:password123"
```

You can choose to only output when a warning condition is met, for example
you've used over 250 minutes:

```
$ vodafone-scraper alert --minutes=250
```

Rather than using ``--auth`` you can store ``VODAFONE_USERNAME`` and
``VODAFONE_PASSWORD`` in your environment:

```
export VODAFONE_USERNAME="me@myemail.com"
export VODAFONE_PASSWORD="<my password"
$ vodafone-scraper show
```

# Running Headless (without a GUI)

You could use ``Xvfb`` to load the Firefox process in a fake X session. See the 
``examples/`` directory for a sample shell script and crontab file to achieve
this.
