#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import api
import constants
from time import sleep

pars = {
	'out': 1,
	'count': 1000,
	}
friends_to_del = api.query(u'friends.getRequests', pars)
friends_to_del = friends_to_del['response']['items']
for friend in friends_to_del:
	pars = {'user_id': friend}
	res = api.query(u'friends.delete', pars)
	print res
	sleep(0.3)


