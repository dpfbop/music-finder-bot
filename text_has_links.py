#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import codecs

def text_has_links(text):
    '''
    Returns False if url founs in text.
    Returns True when everything is OK.
    '''
    f = codecs.open('/var/iris/resources/domains.txt', encoding='utf-8')
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
    text = text.lower()
    text = text + u' '
    mtc = re.search(rstr, text)
    if mtc is not None:
        return True
    else:
        return False

if __name__ == '__main__':
    print text_has_links(u'lol')
    print text_has_links(u'биток.рф ываыва jglskdng l')
    print check_urls(u'vk.com')
    print check_urls(u'fsdfn skj sdfvk.info')
    print check_urls(u'lola.rdfs fdjslk.camera* fjsdifj')
