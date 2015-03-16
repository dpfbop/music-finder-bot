#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import text_utils
import config
#always add lowercase translations
cmd_translated = {
    'bot_name': config.BOT_NAMES,
    'help': [u'help', u'помощь', u'команды'],
    'translate': [u'translate', u'перевод', u'tr', u'словарь', u'dict', u'dictionary'],
    'vanga': [u'предсказамус', u'предскажи', u'предсказание', u'vanga', u'навангуй', u'ванга', u'правда?', u'правда', u'правда,', u'подскажи', u'хочешь'],
    'uzbagoin': [u'узбагойся', u'успокой', u'uzbagoin', u'узбагой'],
    'anonmessage': [u'anonmessage', u'анонимно', u'private'],
    'song': [u'song', u'песня', u'спой', u'музыку', u'музыка', u'песню', u'поиск', u'найди'],
    'videos': [u'videos', u'видео', u'смотреть'],
}


def translate_locale(cmd, dic=cmd_translated):
    l_cmd = text_utils.remove_extra_symbols(cmd, True)
    for command in dic.keys():
        possible_aliases = dic[command]
        if l_cmd in possible_aliases:
            return command
    return False
