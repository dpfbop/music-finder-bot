#!/usr/bin/python
# -*- coding: utf-8 -*-
from db import *
import config
import codecs
import re

def remove_links(text):
    '''
    Removes links from text
    '''
    mod_text = text
    f = codecs.open(config.DOMAINS_FILE, encoding='utf-8')
    domains = []
    for line in f:
        domains.append(line.strip())
    rstr = u'('
    for d in domains:
        rstr += u'\\.' + unicode(d) + u'\W' + u'|'
    del domains
    f.close()
    rstr = rstr[:-1]
    rstr += u')'
    text = text.lower() + u' '
    mtc = re.search(rstr, text)
    while mtc:
        if mtc is not None:
            mod_text = mod_text[0:mtc.start()] + u'(dot)' + mod_text[mtc.start() + 1:]
            text = text[0:mtc.start()] + u'(dot)' + text[mtc.start() + 1:]
        mtc = re.search(rstr, text)
    return mod_text


def levenstein_dist(s, t):
    n, m = len(s), len(t)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        s, t = t, s
        n, m = m, n
 
    current_row = xrange(n+1) # Keep current and previous row, not entire matrix
    for i in xrange(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in xrange(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if s[j-1] != t[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
 
    return current_row[n]


def remove_extra_symbols(text, only_letters=False):
    text = text.lower()
    if only_letters:
        text = re.sub(u'[^a-zа-я0-9 ]', u'', text)
        return text
    ntext = u''
    for symb in text:
        if ord(symb) > 9000:
            ntext += u'&#' + unicode(ord(symb)) + u';'
        else:
            ntext += symb
    text = re.sub(u'[^a-zа-я0-9/#&; ]', u' ', ntext)
    text = u' '.join(text.split())
    return text
