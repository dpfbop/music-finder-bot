#!/usr/bin/python
# -*- coding: utf-8 -*-
import config
from db import db
class CommandTemplate(object):
    def __init__(self, title=u'Default command', enabled=False, hidden=True, help_string=u'', help_examples=[], look_for_help=True):
        self.title = title
        self.enabled = enabled
        self.hidden = hidden
        self.help_string = help_string
        self.help_examples = help_examples
        self.look_for_help = look_for_help
        if title != u'Общение с Ирис':
            cmd = db.commands.find_one({'title': title})
            if not cmd:
                cmd = {'title': title, 'enabled': enabled, 'hidden': hidden, 
                    'help_string': help_string, 'help_examples': help_examples}
                db.commands.insert(cmd)

    def renderhelp(self):
        ans_list = []
        ans_list.append(self.title)
        ans_list.append(self.help_string)
        ans_list.append(u'Примеры:')
        ans_list = ans_list + [config.BOT_NAMES[0] + u' ' + el for el in self.help_examples]
        return u' <br> &#9989;'.join(ans_list)


    def checkerrors(self):
        if self.hidden and int(self.dialog.last_message.user_id) not in config.ADMIN_IDS:
            return u'Команда недоступна для вас. '
        if not self.enabled:
            return u'Команда не работает.'
        return None

    def execute(self):
        error = self.checkerrors()
        if error is not None:
            return self.dialog.answer(error)

        if self.look_for_help:
            args = self.dialog.last_message.args
            if len(args) > 0 and args[0].lower() == u'помощь': #поменяй на locale_translation
                return self.dialog.answer(self.renderhelp())

        self.run()
