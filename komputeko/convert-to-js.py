#!/usr/bin/env python
# Converts Paul Denisowski's ESPDIC project to JS array format.
# The resulting file shares the same license as ESPDIC: CC-BY-3.0.

import re
import glob

for fname in glob.glob('Komputeko-*.txt'):
    komputeko = open(fname, 'r')
    js = open(fname.lower().replace('.txt', '.js').replace('eo.','.'), 'w')
    print fname
    
    lang = fname[10:12]

    print >>js, '// (C) komputeko.net, licensed under CC-BY-SA'
    print >>js, "'use strict';"
    print >>js, 'var komputeko_%s = [' % (lang)

    eo = 0
    alt = 0
    # Each line thereafter contains something like a word and a definition.
    for line in komputeko.readlines():
        if line.strip() == "":
            continue
        if re.search("Komputeko - www.komputeko.net", line):
            eo = 0
            alt = 0
            continue
        if line[0] == " ":
            continue
        match = re.match("(EN) +(EO)", line)
        if match:
            eo = match.start(2)
            continue
        
        enword = line[0:eo-1].strip()
        eoword = line[eo:]
        match = re.search("^(.*)  +(.*)$", eoword)
        if match:
            print >>js, '["%s","%s"],' % (match.group(1).strip(),  enword)
            print >>js, '["%s","%s"],' % (match.group(2).strip(),  enword)
        else:
            print >>js, '["%s","%s"],' % (eoword.strip(),  enword)
        continue

    print >>js, '];'

    # Construct a lowercase version of komputeko.
    # Done on load since it's very fast, even on phones.
    # Chrome seems to not like a.map(String.prototype.toLowerCase).
    print >>js, 'var komputeko_%s_lower = komputeko_%s.map(function(a) { return a.map(function(x) { return x.toLowerCase(); }) });' % (lang, lang)

    komputeko.close()
    js.close()
