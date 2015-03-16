#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

import requests


class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Словарь', True, False, \
            u'Русско-английский и англо-русский словарь, основанный на Яндекс.Словари.', \
            [u'перевод рибосома', u'translate levitation'])

        self.dialog = dialog

    def run(self):
        def slovari_api_request(request, lang='en-ru'):
            translate_key = 'dict.1.1.20130922T204642Z.528c3a276cd0a4da.d2b72d84152bc5051c2c4cafbbe259fef236eb1b'
            translate_api  = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'
            pars = {
                'key': translate_key,
                'lang': lang,
                'text': request
            }
            try:
                r = requests.get(translate_api, params=pars)
            except:
                return('-1')
            response = r.json()
            rdef = response['def']
            if len(rdef) == 0:
                return ('-1')
            meaning = rdef[0]
            translation = meaning['tr'][0]['text']
            return unicode(translation)

        dialog = self.dialog
        args = dialog.last_message.args
        if len(args) == 0:
            return dialog.answer(u'Пожалуйста, введите слово для перевода')
        request = args[0]
        en_ru_tr = slovari_api_request(request, 'en-ru')
        ru_en_tr = slovari_api_request(request, 'ru-en')
        if en_ru_tr == '-1' and ru_en_tr == '-1':
            dialog.answer(u'Не найдено подходящего перевода.')
        elif en_ru_tr != '-1':
            dialog.answer(unicode(en_ru_tr))
        else:
            dialog.answer(unicode(ru_en_tr))


        