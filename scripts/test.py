import re

string = 'http://goes.gsfc.nasa.gov/goeseast/great_lakes/ir4/'
pattern = re.compile(r'http://goes.gsfc.nasa.gov/')
match = pattern.search(string)
prelen = len (match.group(0))
subpath = string[prelen:]
print subpath