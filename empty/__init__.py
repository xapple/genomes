"""
============
Introduction
============
The empty software is a package written in Python. It is designed to be a template.

============
Installation
============
To install you can simply type::

    $ sudo easy_install empty

If you don't have permission to install it like that, you can simply download the code and include the directory in your python path::

    $ wget http://pypi.python.org/packages/source/e/empty/empty-1.0.0.tar.gz
    $ tar -xzf empty-1.0.0.tar.gz
    $ cd empty-1.0.0/
    $ sed -i "$ a\export PYTHONPATH=`pwd`/:\$PYTHONPATH" ~/.bashrc
    $ source ~/.bashrc

========
Examples
========
Here is a way to use it::

    import empty
    empty.Empty()
"""

b'This module needs Python 2.6 or later.'

# Special variables #
__version__ = '1.0.0'

# Built-in modules #
import sys

################################################################################
class Empty(object):
    """Doesn't do anything."""

    def __init__(self):
        sys.exit()
