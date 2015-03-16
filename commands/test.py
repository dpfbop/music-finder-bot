#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
from utils import api

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Тестовая', True, True )
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        ans = dialog.messages[0].body
        dialog.answer(ans)
