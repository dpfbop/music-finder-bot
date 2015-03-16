#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from BeautifulSoup import BeautifulSoup
import requests

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Башорг', True, False, \
            u'Присылает цитату с сайта bash.im', [u'баш', u'башим' , u'цитату'])      
        self.dialog = dialog

    def run(self):
        def get_rating(quote):
            quote = unicode(quote)
            i = quote.find(u'\"rating\">') + 9
            res = u''
            quote = quote[i:]
            siz = quote.find(u'</span')
            for i in xrange(siz):
                res += quote[i]
            return res
        def get_quote(quote):
            quote = unicode(quote)
            i = quote.find(u'class=\"text\"') + 13
            res = u''
            quote = quote[i:]
            siz = quote.find(u'</div')
            for i in xrange(siz):
                res += unicode(quote[i])
            return res
        dialog = self.dialog
        try:
            r = requests.get(u'http://bash.im/random', timeout=3)
        except Exception as e:
            return dialog.answer(u'Произошла ошибка при подключении к bash.im')
        quote_text = ''.join(r.text)
        soup = BeautifulSoup(quote_text)
        quotes = soup.findAll("div", { "class" : "quote"})
        formatted_quotes = []
        for quote in quotes:
            rating_quote = get_rating(quote)
            text_quote = get_quote(quote)
            if (rating_quote != u'' and rating_quote != u' ... '):
                formatted_quotes.append((rating_quote, text_quote))
            #if (rating_quote != ""):
            #    formatted_quotes.append((rating_quote, text_quote))
        max_rating = int(formatted_quotes[0][0])
        max_quote = formatted_quotes[0]
        for quote in formatted_quotes:
            if (int(quote[0]) > max_rating):
                max_rating =  int(quote[0])
                max_quote = quote
        answ = max_quote[1]
        answ = answ.replace(u'<br />', u'<br>')
        answ = answ.replace(u'&quot;', u'"')  
        answ = answ.replace(u'&gt;', u'>')
        answ = answ.replace(u'&lt;', u'<')
        return dialog.answer(answ)
