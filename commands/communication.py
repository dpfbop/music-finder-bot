#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
import constants 

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Общение с Ирис', True, False)      
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        ans = dialog.last_message.args
        ans = ans.split(constants.SPLIT_SIGN)
        attach = u','.join(ans[1:])
        dialog.answer(ans[0], attachment=attach)
