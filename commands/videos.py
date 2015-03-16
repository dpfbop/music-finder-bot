#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from utils import api
from smiles import *

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Видео', True, False, \
            u'Поиск видео по вашему запросу. Идеально подходит для бесед с друзьями! ', 
            [u'видео шерлок'])
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        message = dialog.last_message
        args = message.args
        if len(args) == 0:
            return dialog.answer(u'Пустая строка запроса. ')
        req = u' '.join(args)
        pars = {
            'q': req,
            'sort': 2,
            'adult': 0,
        }
        r = api.query(u'video.search', pars)
        vids = r.get('response')
        if vids is None:
            return dialog.answer(u'Ничего не найдено ' + smiles['sad'])
        vids = vids.get('items')
        kol = min(len(vids), 4)
        if kol == 0:
            return dialog.answer(u'Ничего не найдено ' + smiles['sad'])
        respstr = u''
        for i in xrange(kol):
            respstr += u'video' + unicode(vids[i]['owner_id']) + u'_' + unicode(vids[i]['id']) + u','
        dialog.answer(u'Приятного просмотра! ' + smiles['smile'], respstr)
