#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from tokens import get_token
import logger
import traceback

def query(method, args={}, lana=False, timeout=None, verify_ssl=True, bot=None):
    pars = args
    pars['access_token'] = unicode(get_token(bot))
    pars['v'] = args.get('v', '5.14')
    if lana == True:
        pars['access_token'] = unicode(get_token(bot))

    prefix = 'https://api.vk.com/method/'
    if timeout is None:
        if method in ['messages.get']:
            timeout = 0.5
        else:
            timeout = 2
    try:
        r = requests.get(unicode(prefix + method), params=pars, timeout=timeout, verify=verify_ssl)
    except Exception as e:
        logger.error(str(e))
        return None
    try:
        r = r.json()
    except:
        logger.error(u'Не получилось раскодировать json из ответа ВК.\n' + r.text)
        return None

    if r.get('error') is not None:
        return r
    elif r.get('response') is not None:
        return r
    else:
        print r.text
        logger.error(u'Непонятный ответ от ВК:\n' + r.text)
        return None
