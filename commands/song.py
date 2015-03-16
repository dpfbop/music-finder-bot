#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
from utils import api
import constants
from smiles import smiles

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Песня', True, False, \
            u'Присылает песню, рекомендованную вам, если ваши аудиозаписи открыты. Иначе отправит просто хорошую песню. ', \
            [u'песню', u'музыка'])
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        if len(args) > 0:
            query = u' '.join(args)
        else:
            query = None
        if query:
            pars = {
                'query': query
            }
            r = api.query(u'execute.search_songs', pars, bot=dialog.bot)
            audio = r["response"]
            return dialog.answer(u'Найдено по запросу "' + query + u'":', audio)
        else:
            pars['user_id'] = config.MUSIC_ID
            r = api.query(u'execute.song', pars, bot=dialog.bot)
            audio = r["response"]
            return dialog.answer(u'Рекомендовано вам :)', unicode(audio))
