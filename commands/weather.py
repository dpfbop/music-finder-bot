#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
import re
import requests

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Погода', True, False, \
            u'Команда присылает погоду в нужном городе на данный момент.', \
            [u'погода Москва', u'погода лondon' , u'погода екатеринбург'])
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        if len(args) == 0:
            return dialog.answer(u'Пожалуйста, введите город после слова "погода". ')
        city = unicode(args[0]).lower()
        pars = {
            'q': city,
            'units': 'metric',
            'lang': 'ru', 
        }
        try:
            r = requests.get(u'http://api.openweathermap.org/data/2.5/weather', params=pars, timeout=5)
            r = r.json()
            if str(r['cod']) != '200':
                return dialog.answer(u'Введенный город не найдет, попробуйте указать точное название. ')
            answer = u''
            answer += u'Погода в ' + unicode(r['name']) + u', ' + unicode(r['sys']['country']) + u'.<br>'
            answer += unicode(r['main']['temp']) + u' °C. '
            if r.get('weather'):
                answer += unicode(r['weather'][0]['description']).strip().capitalize()
            answer += u'<br>'
            answer += u'Давление: ' + unicode(round(float(r['main']['pressure']) / 1.3332, 2)) + u' мм рт. ст. <br>'
            answer += u'Влажность: ' + unicode(r['main']['humidity']) + u'%<br>'
            answer += u'Облачность: ' + unicode(r['clouds']['all']) + u'%<br>'
            return dialog.answer(answer)
        except:
            return dialog.answer(u'Ошибка во время запроса к сервису погоды. ')
