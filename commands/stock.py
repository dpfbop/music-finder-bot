#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
import re
import requests

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Биржа', True, False, u'Курсы валют/криптовалют с биржи BTC-E. ', \
        	[u'курс доллар', u'курс euro usd' , u'курс ltc'])
        self.dialog = dialog

    def run(self):
	    def conv(request_string):
	        request_cases = {
	        u'ltc': [u'лайт.*', u'lite.*', u'лтц.*', u'^л$'],
	        u'btc': [u'бит.*', u'bit.*'],
	        u'rur': [u'руб.*', u'rub.*', u'копейк.*'],
	        u'usd': [u'долл.*', u'usd.*', u'dollar.*'],
	        u'eur': [u'eur.*', u'евро.*'],
	        }
	        for k in request_cases.keys():
	            for reg in request_cases[k]:
	                found = re.search(reg, request_string, re.UNICODE)
	                if found is not None:
	                    return k
	        return False

	    def btce_request(request):
	        btce_api= u'https://btc-e.com/api/2/' + request + u'/ticker'

	        try:
	            r = requests.get(btce_api, timeout=2)
	        except requests.exceptions.ConnectionError:
	            return False
	        try:
	            response = r.json()
	            ticker = response['ticker']
	        except Exception as e:
	            return False
	        return ticker

	    dialog = self.dialog
	    args = dialog.last_message.args
	    if len(args) == 0:
	        return dialog.answer(u'Пожалуйста, введите пару валют после команды курс')
	    first = args[0]
	    second = u'rur'
	    if len(args) > 1:
	        second = args[-1]
	    tmp = conv(first)
	    first = tmp if tmp else first
	    tmp = conv(second)
	    second = tmp if tmp else second
	    ticker = {}
	    if first == u'eur' and second == u'rur':
	        ticker1 = btce_request(first + u'_usd')
	        ticker2 = btce_request(u'usd_rur')
	        ticker['last'] = unicode(float(ticker1['last']) * float(ticker2['last']))
	    else:
	        ticker = btce_request(first + u'_' + second)

	    if not ticker:
	        dialog.answer(u'Неверные валюты или ошибка во время запроса к бирже BTC-E')
	    else:
	        ans = u'' + unicode(ticker['last']) + u' ' + unicode(second) + u' <br>' 
	        if first == u'ltc' or first == u'btc':
	            ans = u'Last: ' + unicode(ticker['last']) + u' ' + unicode(second) + u' <br>' + \
	                u'High: ' + unicode(ticker['high']) + u' ' + unicode(second) + u' <br>' + \
	                u'Low: ' + unicode(ticker['low']) + u' ' + unicode(second) + u' <br>' + \
	                u'Volume: ' + unicode(ticker['vol']) + u' ' + unicode(second) + u' <br>'
	        dialog.answer(ans)
