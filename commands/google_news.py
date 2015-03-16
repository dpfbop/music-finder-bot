#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

import config
import requests
from locale_translation import *
import xml.etree.ElementTree as ET

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Новости', True, False, \
            u'Google News. <br> Можно задать секцию: <br>    мир, бизнес, россия, наука, спорт <br>', \
            [u'новости', u'новости спорт'])

        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        pars = {
            'pz': '1',
            'cf': 'all',
            'ned': 'ru_ru',
            'hl': 'ru',
            'output': 'rss'
        }

        if len(args) > 0:
            sect = args[0]
            sect = translate_locale(sect, news_sections)
            if not sect:
                return dialog.answer(u"Нет такой секции. Помощь вам в помощь.")
            pars['topic'] = sect

        google_rss = "https://news.google.com/news/feeds"

        try:
            r = requests.get(google_rss, params=pars)
        except requests.exceptions.ConnectionError:
            return dialog.answer(u'Не могу достучатсья до google news')

        #feed = requests.get('https://news.google.com/news/feeds?pz=1&cf=all&ned=ru_ru&hl=ru&topic=b&output=rss')
        feed = ET.fromstring(r.text.encode('utf-8'))

      #res = []
        ans  = ""
        cnt = 0
        temp = ""
        for entry in feed.iter('item'):
            cnt += 1
            if cnt > config.NUMBER_OF_NEWS:
                break
            about = entry.find('title').text
            about = about.replace('.Ru', u'.Ру').replace('.ru', u'.ру').split("-")
            about = about[:-1]
            if u'РБК' in about[-1]:
                about = about[:-1]
            about = '-'.join(about)

            temp += unicode(u'&#128313; ' + about + '<br>')
        ans = temp + "https://news.google.ru/news/section?&topic=" + pars.get('topic', '')
        return dialog.answer(unicode(ans))
