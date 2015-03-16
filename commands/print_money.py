#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from common_db import cdb
from utils import vk_utils

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Деньги', True, False, u'Выводит количество монет на вашем счету. ', \
            [u'деньги'])
        self.dialog = dialog

    def run(self):
        user = vk_utils.get_users(self.dialog.last_message.user_id)[0]
        self.dialog.answer(u'У вас ' + unicode(user['money']) + u' монет.<br> Удачных покупок!')

