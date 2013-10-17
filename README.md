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
$ vodafone-scraper --user=me@myemail.com "--password=password123"
```
