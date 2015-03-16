#!/usr/bin/python
# -*- coding: utf-8 -*-
import config
def get_token(bot=None):
    if bot == None:
        return config.LANA_TOKEN
    else:
        return bot.access_token
