#!/usr/bin/python
# -*- coding: utf-8 -*-
from locale_translation import *
import random
from db import db
from common_db import cdb
import logger
import importlib
from utils import communication_utils, api, vk_utils
import config
import time
import commands
import os
import traceback

class Bot(object):
    def __init__(self):
        bot_name = os.path.abspath(__file__).split('/')[-2]
        bot = cdb.bots.find_one({'name': bot_name})
        if bot is None:
            logger.error('No info about bot in database, aborting.')
            exit(0)
        self.id = bot['id']
        self.access_token = bot['access_token']
        self.name = bot['name']
        self.enabled = bot['enabled']
        self.only_with_name = bot['only_with_name']
        self.priority = bot['priority']


class Dialog(object):
    def __init__(self, message):
        dialog_id = message.dialog_id
        dialog = db.dialogs.find_one({'dialog_id': dialog_id})

        if dialog is None:
            dialog = {}
            dialog['dialog_id'] = dialog_id
            dialog['messages'] = []


        if len(dialog['messages']) >= 10:
            messages = dialog['messages']
            messages.sort(key=lambda x: x['date'])
            dialog['messages'] = messages[1:]

        self.bot = message.bot
        bot = message.bot
        del message.bot
        dialog['messages'].append(message.__dict__)
        dialog['last_message'] = message.__dict__
        db.dialogs.save(dialog)

        self.dialog_id = dialog_id
        self.messages = [Message(m, bot) for m in dialog['messages']]
        self.last_message = message


    def run(self):
        cmd = self.last_message.function
        cmd = getattr(commands, cmd).Command(self) #переписать этот говнокод!
        try:
            res = cmd.execute()   #подумай, можно ли лучше
            if res is None:
                return True
            else:
                return res
        except:
            logger.error(traceback.format_exc())
            return False


    def answer(self, text, attachment=None, domain=None, title=None):
        receiver = 'chat_id' if self.dialog_id < 0 else 'user_id'
        receiver_id = abs(self.dialog_id)
        pars = {
            'message': text,
            receiver: unicode(receiver_id),
            #'access_token': tokens.get_token(),
            'guid': random.randint(0, 1000000),
        }

        if attachment is not None:
            pars['attachment'] = attachment
        if title is not None:
            pars['title'] = title
        if domain is not None:
            del pars[receiver]
            pars['domain'] = domain

        response = api.query(u'messages.send', args=pars, bot=self.bot)
        info = vk_utils.get_bot_info()
        if info is None:
            logger.err(u'Не удалось получить информацию о боте, ответ не отправлен. ')
            return None
        if response is None:
            logger.log(u'Ничего не пришло в ответ от Vk в classes.py@answer')
            return response
        if response.get('error') is None:
            if info['status'] != 'ok':
                #api.query(u'account.setOnline')
                vk_utils.set_bot_status(info, 'ok')
        else:
            logger.log(u'Пришла ошибка от VKAPI во время отправки сообщения. ' \
                + unicode(response['error']['error_msg'])) 
            if response['error']['error_code'] == 14: 
                vk_utils.set_bot_status(info, 'error', response['error']['captcha_sid'])

        return response


class Message(object):
    def __init__(self, vk_response, bot):
        self.prefix = u'https://api.vk.com/method'
        self.id = vk_response['id']
        self.dialog_id = vk_response['user_id']
        if vk_response.get('chat_id') is not None:
            self.dialog_id = -int(vk_response.get('chat_id'))
        self.user_id = vk_response['user_id']
        self.chat_id = vk_response.get('chat_id')
        self.body = vk_response['body']
        self.words = self.body.split()
        self.date = vk_response['date']
        self.fwd_messages = vk_response.get('fwd_messages')
        self.attachments = vk_response.get('attachments')
        self.function = None
        self.args = []
        self.bot = bot
        #self.identify_command()


    def decode(message):
        return Message(message)


    def is_mine(self):
        if self.bot.only_with_name or self.dialog_id < 0:
            return (u'bot_name' == translate_locale(self.words.get(0)))
        return True

    def identify_command(self):
        request = self.words
        if len(request) == 0:
            self.function = 'communication'
            self.args = u'Привет, я чат-бот!'
            return
        if translate_locale(self.words[0]) == u'bot_name':
            request = self.words[1:]
        cmd = False
        if len(request) > 0:
            cmd = translate_locale(request[0])

        if not cmd:
            #ans = communication_utils.find_answer(u' '.join(request))
            self.function = ''
            self.args = u''
            return

        self.function = cmd
        self.args = request[1:]


    def mark_as_read(self):
        TIME_TO_READ = 5
        now = time.time()

        mid = self.id
        #to_mark = db.mark_as_read.find_one()
        global MESSAGES_TO_MARK_AS_READ
        if 'MESSAGES_TO_MARK_AS_READ' not in globals():
            MESSAGES_TO_MARK_AS_READ = [-now]
        MESSAGES_TO_MARK_AS_READ.append(mid)

        start_from = -MESSAGES_TO_MARK_AS_READ[0]
        if start_from <= 0 or now - start_from >= config.TIME_TO_MARK_AS_READ:
            to_mark_str = ','.join(map(str, MESSAGES_TO_MARK_AS_READ[1:]))
            api.query('messages.markAsRead', {'message_ids': to_mark_str}, timeout=0.03, verify_ssl=False)
            #r = requests.get(self.prefix + 'messages.markAsRead', params=pars)
            #html = json.loads(r.text)
            MESSAGES_TO_MARK_AS_READ = [-now]
            
    def finilize(self):  #what to do when destroying massage
        pass
