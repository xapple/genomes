"""
============
Introduction
============
The **genomes** software is a package written in Python. It is designed to provide easy access to some meta data about genome assemblies. You can retrieve the list of chromosomes for any assembly. In addition, you can get the lengths in base pairs of every chromosome.

============
Installation
============
To install you can simply type::

    $ sudo easy_install genomes

If you don't have permission to install it like that, you can simply download the code and include the directory in your python path::

    $ wget http://pypi.python.org/packages/source/g/genomes/genomes-1.0.0.tar.gz
    $ tar -xzf genomes-1.0.0.tar.gz
    $ cd genomes-1.0.0/
    $ sed -i "$ a\export PYTHONPATH=`pwd`/:\$PYTHONPATH" ~/.bashrc
    $ source ~/.bashrc

========
Examples
========
Here are all the things you can do with it::

    from genomes import Assembly
    a = Assembly('sacCer2')
    print a.chrmeta
    print a.guess_chromsome_name('chr1')
"""

b'This module needs Python 2.6 or later.'

# Special variables #
__version__ = '0.0.0-1-g9eaf3db'

################################################################################
class Assembly(object):
    """The only object provided by the library.

       :param assembly: Aa valid assembly name.
       :type  assembly: string
    """

    def __init__(self, assembly):
        pass

    @property
    def chromosomes(self):
        """A list of chromsome dicitonaries."""
        return None

    @property
    def chrmeta(self):
        """A dictionary of chromosome metadata::

            >>> from genomes import Assembly
            >>> a = Assembly('TAIR10')
            >>> print a.chrmeta
            {'c': {'length': 154478}, 'm': {'length': 366924}, '1': {'length': 30427671}, '3': {'length': 23459830}, '2': {'length': 19698289}, '5': {'length': 26975502}, '4': {'length': 18585056}}
        """
        return None

    def guess_chromosome_name(self, chromosome_name):
        """Searches the assembly for chromosome synonym names,
           and returns the canonical name of the chromosome.
           Returns None if the chromosome is not known about.

           :param chromosome_name: Any given name for a chromosome in this assembly.
           :type  chromosome_name: string

           :returns: The same or an other name for the chromosome.

           ::

               >>> from track import genrep
               >>> a = genrep.Assembly('sacCer2')
               >>> print a.guess_chromosome_name('chrR')
               2micron
        """
        return None

################################################################################
if __name__ == "__main__":
    import doctest
    doctest.testmod()
