#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from smiles import *
import requests

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Шутка', True, False, \
            u'Просто рассказывает шутку (вероятно смешную).', [u'шутка', u'рассмеши' , u'анекдот'])      
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        pars = {
                'format': 'json',
                'type': 'random',
                'amount': '1',
            }
        r = requests.get('http://shortiki.com/export/api.php', params=pars) 
        try:
            joke = r.json()[0]['content']
        except:
            return dialog.answer(u'Ошибка во время получения анекдота :(')
        joke += u'<br>Если там &#128070; что-то плохое, то это не моя вина ' + smiles['smile']
        return dialog.answer(unicode(joke))