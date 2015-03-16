#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from smiles import *
import requests
from db import db


class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Помощь', True, False, \
            u'Команда "помощь" выводит список доступных команд. ', [u'помощь'])      
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        commands = db.commands.find({'enabled': True, 'hidden': False})
        ans = u'Доступные команды:' + u'\n' + u'\n'.join(sorted([u'&#9989; ' + el['title'] for el in commands]))
        return dialog.answer(ans)