#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import random
from db import db
import tokens
import constants
from utils import api
from datetime import datetime
from datetime import timedelta
import time
import logger

active_dialogs = list(db.dialogs.find(fields=['last_message', 'dialog_id']))
now = datetime.now()

params = {
        'count': 1,
        'preview_length': 1,
        'unread': 1,
        'offset': 0,
}
amo = api.query(u'messages.getDialogs', params)['response']['count']
print amo
params['count'] = 200
dialogs = []
for i in xrange(0, amo + 2, 200):
    time.sleep(0.5)
    params['offset'] = i
    try:
        r = api.query(u'messages.getDialogs', params)['response']['items']
        for el in r:
            if el['message'].get('chat_id'):
                dialogs.append(el['message']['chat_id'])
    except Exception as e:
            logger.log(u'Ошибка во время получения диалогов. ' + unicode(e))
            print e
            continue


print 'dialogs found:' + str(len(dialogs))
print 'active_dialogs: ' + str(len(active_dialogs))

should_be_deleted = []

for d in dialogs:
    ok = False
    for dd in active_dialogs:
        date = datetime.fromtimestamp(dd['last_message']['date'])                
        if dd['dialog_id'] == -d:
            ok = True
        if dd['dialog_id'] == -d and date + timedelta(days=constants.DAYS_BEFORE_LEAVING_THE_DIALOG) < now:
            should_be_deleted.append(d)
    if not ok:
        should_be_deleted.append(d)

print 'should be deleted dialogs: ' + str(len(should_be_deleted))
for chat_id in should_be_deleted:
    time.sleep(0.75)
    r = api.query(u'messages.removeChatUser', {'chat_id': chat_id, 'user_id': constants.BOT_ID })
    print r
