#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
from config import ERROR_FILE, LOG_FILE
from datetime import datetime

def log(text):
    with codecs.open(LOG_FILE, 'a+', encoding='utf-8') as log:
        time = str(datetime.now())
        if not isinstance(text, unicode):
            text = unicode(text, 'utf-8', 'replace')
        message = '\n' + '#'*40 + '\n' + time + '\n' + text + '\n'
        log.write(message)

def error(text):
    with codecs.open(ERROR_FILE, 'a+', encoding='utf-8') as error:
        time = str(datetime.now())
        if not isinstance(text, unicode):
            text = unicode(text, 'utf-8', 'replace')
        message = '\n' + '#'*40 + '\n' + time + '\n' + text + '\n'
        error.write(message)
