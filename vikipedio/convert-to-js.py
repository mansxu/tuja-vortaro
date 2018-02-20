#!/usr/bin/env python
# Converts Paul Denisowski's ESPDIC project to JS array format.
# The resulting file shares the same license as ESPDIC: CC-BY-3.0.

import re
import glob

for fname in glob.glob('vikipedio-*.out'):
	vikipedio = open(fname, 'r')
	js = open(fname.replace('.out', '.js'), 'w')
	print fname
	
	lang = fname[10:12]

	print >>js, '// Wikipedia Foundation, CC-BY-3.0.'
	print >>js, "'use strict';"
	print >>js, 'var vikipedio_%s = [' % (lang)

	# Each line thereafter contains something like a word and a definition.
	for line in vikipedio.readlines():
	    line = line.replace('"', '\\"')

	    arr = line.strip().split('|')
	    if len(arr) != 2:
		continue
	    esperanto, alia = arr

	    print >>js, '["%s","%s"],' % (esperanto,  alia)

	print >>js, '];'

	# Construct a lowercase version of vikipedio.
	# Done on load since it's very fast, even on phones.
	# Chrome seems to not like a.map(String.prototype.toLowerCase).
	print >>js, 'var vikipedio_%s_lower = vikipedio_%s.map(function(a) { return a.map(function(x) { return x.toLowerCase(); }) });' % (lang, lang)

	vikipedio.close()
	js.close()
