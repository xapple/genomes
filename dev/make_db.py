"""
A script that generates the database.
"""

################################################################################
class JsonJit(object):
    """
    JsonJit is a class for Just In Time instantiation of JSON resources.
    The __lazy__ method downloads the JSON resource from the server.
    But the __lazy__ method is called only when the first attribute is either get or set.
    You can use it like this:

        assemblies = JsonJit('http://bbcftools.vital-it.ch/genrep/assemblies.json', 'assembly')

    :param url: Location of the JSON to load
    :param list_key: Optional dictionary key to unpack the elements of JSON with
    """

    def __init__(self, url, list_key=None):
        """Save the passed parameters"""
        self.__dict__['url'] = url
        self.__dict__['list_key'] = list_key
        self.__dict__['obj'] = None

    def __lazy__(self):
        """Fetch resource and instantiate object."""
        import json, urllib2
        try:
            content = urllib2.urlopen(self.url).read()
            # Create the child object #
            self.__dict__['obj'] = json.loads(content)
        except urllib2.URLError as err:
            self.__dict__['obj'] = err
        # Unpack the child object #
        if self.list_key:
            for num, item in enumerate(self.obj):
                self.obj[num] = item[self.list_key]

    def get(self, value):
        """Retrieve an item from the JSON
           by searching all attributes of all items
           for *name*"""
        if not self.obj: self.__lazy__()
        for x in self.obj:
            if [k for k,v in x.items() if v == value]: return x

    def filter(self, key, value):
        """Retrieve an item from the JSON
           by search a key that is equal to value in
           all elements"""
        if not self.obj: self.__lazy__()
        return [x for x in self.obj for k,v in x.items() if v == value and k == key]

    def by(self, name):
        """Return a list of attributes present
           in every element of the JSON"""
        if not self.obj: self.__lazy__()
        return [x or x.encode('ascii') and isinstance(x, basestring) for x in [x.get(name) for x in self.obj]]

    def make(self, name):
        """Return an object whoes attributes are the
           keys of the element's dictionary"""
        if not self.obj: self.__lazy__()
        class JsonObject(object): pass
        obj = JsonObject()
        obj.__dict__.update(self.get(name))
        return obj

    def __getattr__(self, name):
        """Method called when an attribute is
           not found in __dict__."""
        if not self.obj: self.__lazy__()
        # Search in the child object #
        try: return getattr(self.obj, name)
        except AttributeError:
            # Search in the parent object #
            if name in self.__dict__: return self.__dict__[name]
            else: return self.make(name)

    def __setattr__(self, name, value):
        """Method called when an attribute is
           assigned to."""
        if not self.obj: self.__lazy__()
        try: setattr(self.obj, name, value)
        except AttributeError: self.__dict__[name] = value

    def __len__(self):
        if not self.obj: self.__lazy__()
        return self.obj.__len__()

    def __iter__(self):
        if not self.obj: self.__lazy__()
        return self.obj.__iter__()

    def __repr__(self):
        if not self.obj: self.__lazy__()
        return self.obj.__repr__()

    def __getitem__(self, key):
        if not self.obj: self.__lazy__()
        return self.obj[key]

    def __setitem__(self, key, item):
        if not self.obj: self.__lazy__()
        self.obj[key] = item

    def __delitem__(self, key):
        if not self.obj: self.__lazy__()
        del self.obj[key]

################################################################################
# Constants #
url = "http://bbcftools.vital-it.ch/genrep/"

# Expose base resources #
organisms     = JsonJit(url + "organisms.json",     'organism')
genomes       = JsonJit(url + "genomes.json",       'genome')
nr_assemblies = JsonJit(url + "nr_assemblies.json", 'nr_assembly')
assemblies    = JsonJit(url + "assemblies.json",    'assembly')
sources       = JsonJit(url + "sources.json",       'source')
chromosomes   = JsonJit(url + "chromosomes.json",   'chromosome')

################################################################################
# Make a db #
import os, sqlite3
path = 'genomes.db'
if os.path.exists(path): os.remove(path)
connection = sqlite3.connect(path)
cursor = connection.cursor()

# Make the assemblies table #
col_names = assemblies[0].keys()
col_string = '(' + ','.join(col_names) + ')'
question_marks = '(' + ','.join(['?' for x in xrange(len(col_names))]) + ')'
cursor.execute("CREATE table assemblies " + col_string)
command = "INSERT into assemblies " + col_string + ' values ' + question_marks
generator = ([a[k] for k in col_names] for a in assemblies)
cursor.executemany(command, generator)

# Make one table per assembly #
base_keys = chromosomes[0].keys()
base_keys.remove('chr_names')
col_names = ['label'] + base_keys
col_string = '(' + ','.join(col_names) + ')'
question_marks = '(' + ','.join(['?' for x in xrange(len(col_names))]) + ')'
for a in assemblies:
    # Get all chromsomes #
    chrs = []
    for ch in chromosomes:
        for data in ch['chr_names']:
            if data['chr_name']['assembly_id'] == a['id']:
                chrs.append([data['chr_name']['value'] + [ch[k] for k in base_keys]])
    # Write it #
    cursor.execute("CREATE table '%s' %s" % (a['name'], col_string))
    command = ("INSERT into '%s' " + col_string + ' values ' + question_marks) % a['name']
    cursor.executemany(command, chrs)
