#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from smiles import *
import requests
import json
import utils
import urllib
from utils import vk_utils

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Википедия', True, False, \
            u'Эта функция дает по запросу небольшой обзор нужной статьи из' + \
            u'википедии и даёт ссылку.', [u'вики Александр 2', u'вики клаустрофобия', u'вики Бунин'])
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        if len(args) == 0:
            #string = 'Пожалуйста, укажите название статьи.' + choice(dic)
            dialog.answer(u'Пожалуйста, укажите название статьи.')
            return
        query = ' '.join(args)
        wiki_api  = 'http://ru.wikipedia.org/w/api.php?'  # А что если нужна не русская вики? очевидно русская, потому что аудитория вк только русская. для гурманов можно ссылку на англ версию при желании
        wiki_main = 'http://ru.wikipedia.org/wiki/'
        pars = {
            'action': 'query',
            'list': 'search',
            'format': 'json',
            #no ' '
            'srsearch': query,
            'srprop': 'snippet',
            'srlimit': '3'
        }

        try:
            r = requests.get(wiki_api, params=pars)  #А что если он не ответит?
        except requests.exceptions.ConnectionError:
            dialog.answer(u'Не могу достучатсья до вики.')
            return
        query      = json.loads(r.text)
        query      = query['query']
        searchinfo = query.get('searchinfo')

        if not searchinfo.get('suggestion') is None:
            return dialog.answer(u'Вы имели в виду ' + unicode(searchinfo.get('suggestion')) + u'?')  #А что если он вернёт пустую строку? suggestion возвращается только если есть

        search = query.get('search')  #А что если он ответит криво? как?
        if len(search) == 0:
            return dialog.answer(u'Ошибка в запросе.')
        title = search[0].get('title')
        if not title:
            return dialog.answer(u'Ошибка в запросе.')
        pars = {
            'action': 'query',
            'prop': 'extracts',
            'format': 'json',
            'titles': title,
            'exintro': '',
            'explaintext': '',
            'indexpageids': ''
        }
        r = requests.get(wiki_api, params=pars)
        query = r.json()
        query = query['query']['pages'][query['query']['pageids'][0]]
        #Добаить ф-цию запроса всего 'extract' сначала нужно понять, почему даже это не работает
        # it doesnt work because of the limit for the length of the message.
        answer = unicode(vk_utils.limit_answer(query['extract'])) + '\n' + wiki_main + urllib.quote(title.replace(' ', '_').encode('utf-8')) 
        dialog.answer(answer)
