#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
#from text_has_links import text_has_links
import time
from utils import text_utils
from db import db
from utils import api
from utils import text_utils
import hashlib
from smiles import smiles
import config


class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Анонимно', True, False, \
            u'Позволяет отправлять анонимные сообщения от лица Ирис (чтобы нести людям добро тайно). ', \
            [u'анонимно id231219001 привет'])
        self.dialog = dialog

    def answer_anon(self):
        fwd = self.dialog.last_message.fwd_messages
        if fwd is None or len(fwd) == 0:
            return self.dialog.answer(u'Пожалуйста, прикрепите анонимное сообщение, на которое хотите ответить.')
        if len(fwd) != 1:
            return self.dialog.answer(u'Пожалуйста, прикрепите только одно сообщение.')

        respond = fwd[0]
        if respond['user_id'] != config.BOT_ID:
            return self.dialog.answer(u'Ой-ой. Мне кажется прикрепленная анонимка не от меня.')
        
        user_id = self.dialog.last_message.user_id
        anon_messages = db.anon_messages
        hashed = hash(respond['body'])
        history = anon_messages.history.find_one({'user_id': user_id, 'hashed': hashed})
        #add time checking here. In case there are same messages.
        if history is None:
            return self.dialog.answer(u'Я не помню такого анонимного сообщения ' + smiles['sad'])

        to_answer = {
            'text': history['text'],
            'anon_id': history['anon_id'],
            'user_name': history['user_name']
        }

        args = self.dialog.last_message.args
        if len(args) <= 1:
            return self.dialog.answer(u'Введите ваше сообщение после слова "ответ".')
        else:
            body = u' '.join(args[1:])
            body = text_utils.remove_links(body)

        text = u'На ваше анонимное сообщение: «' + to_answer['text'] + u'»\n' +\
               unicode(to_answer['user_name']) +\
               u"(id" + unicode(self.dialog.last_message.user_id) + u") ответил: «" 
        text += u"{}»".format(body)

        res = api.query('messages.send', {'user_id': to_answer['anon_id'], 'message': text, 'title': u'Ответ на анонимку'})
        ok = res.get('error')

        time.sleep(0.5)
        if ok is not None:
            self.dialog.answer(u'Ваше сообщение не было отправлено из-за настроек приватности адресата. ')
        else:
            self.dialog.answer(u'Ваш ответ скорее всего уже доставлен:)')

        return res


    def dump_anon(self, sender_id, original, domain, mid):
        message = api.query('execute.get_anon_info', {'domain': domain, 'mid': mid['response']})
        if message is not None:
            r = message.get('response')
        else:
            return None
        
        user_id = r['user']['user_id']
        user_name = r['user']['first_name'] + u' ' + r['user']['last_name']
        anon_text = r['message']['body']
        datte = r['message']['date']

        entry = {
            'user_id': user_id,
            'anon_id': sender_id,
            'text': original,
            'date': datte,
            'user_name': user_name,
            'hashed': hash(anon_text)
        }

        anon_messages = db.anon_messages
        hist = anon_messages.history
        return hist.insert(entry)


    def run(self):
        args = self.dialog.last_message.args
        if len(args) == 0:
            return self.dialog.answer(u'Пожалуйста, введите после слова "анонимно" ссылку на профиль человека Вконтакте, которому предназначено сообщение, а потом само сообщение')
        anonid = unicode(args[0])
        if anonid == u'ответ':
            return self.answer_anon()
        anonid = anonid.replace(u'https://vk.com/', u'')
        anonid = anonid.replace(u'http://vk.com/', u'')
        anonid = anonid.replace(u'vk.com/', u'')
        anonid = unicode(anonid)
        if anonid == u'iris_helper' or anonid == u'id224327479' or anonid == u'eric_helper' or anonid == u'id243758493':
            return self.dialog.answer(u'Мне не нужно ничего писать:Р')
        anonmess = u''
        if len(args) > 1:
            anonmess = u' '.join(args[1:])
            old_anon = anonmess
            anonmess = text_utils.remove_links(anonmess)
            if len(anonmess)!=len(old_anon):
                text_had_links = True
            else:
                text_had_links = False
            original_anonmess = anonmess
            anonmess = u'«' + anonmess + u'», – кто-то написал вам анонимно. \n'
            anonmess += u'\nВы можете ответить на анонимку, написав "анонимно ответ <текст>" и прикрепив это сообщение.'
        else:
            return self.dialog.answer(u'Введите сообщение после ссылки на профиль адресата. ')
        #check if clocked here
        res = self.dialog.answer(unicode(anonmess),domain=anonid, title=u'Анонимное сообщение')
        ok = res.get('error')
        time.sleep(0.5)
        if ok is not None:
            self.dialog.answer(u'Ваше сообщение не было отправлено из-за настроек приватности адресата. ')
        else:
            if text_had_links:
                no_links = u'\nЯ вырезала ссылку из вашего сообщения. Давай больше не будем их отправлять, пожалуйста?:)'
            else:
                no_links = ''
            self.dialog.answer(u'Ваше сообщение доставлено с большой вероятностью :)' + no_links)

            self.dump_anon(self.dialog.last_message.user_id, unicode(original_anonmess), anonid, res)
        return
