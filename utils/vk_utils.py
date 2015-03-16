#!/usr/bin/python
# -*- coding: utf-8 -*-
from utils import api
import config
import time
from utils import text_utils
import logger 
from common_db import cdb

def read_learn_public(public_id, shell):
    amount = 10
    cur = 0
    public = []
    while cur < amount:
        pars = {
            'owner_id': public_id,
            'count': 100,
            'offset': cur,
        }
        is_lana = 1 if config.BOT_LEARN_PUBLIC == config.MAIN_LEARN_PUBLIC else 0
        posts = api.query(u'wall.get', pars, lana=is_lana)
        if posts is None or posts.get('error') is not None:
            cur += 10
            continue
        posts = posts['response']
        amount = posts['count']
        posts = posts['items']
        for post in posts:
            post['text'] = text_utils.remove_extra_symbols(post['text'])
            if shell:
                print post['text']
            questions = [el.strip() for el in post['text'].split(u'//')]
            public.append({
                'id': post['id'], 
                'question': questions[0], 
                'answers': [],
                'same_as': questions[1:]
                })
            params = {
                'owner_id': post['owner_id'],
                'post_id': post['id'],
                'count': 100,
                'need_likes': 1,
            }
            comments = api.query(u'wall.getComments', params, lana=is_lana)
            time.sleep(0.3)
            if comments is None or comments.get('error') is not None:
                time.sleep(0.5)
                comments = api.query(u'wall.getComments', params, lana=is_lana)
            if comments is None or comments.get('error') is not None:
                logger.log(u'Не удалось получить комменты к посту с вопросом: ' + post['text'])
                continue
            comments = comments['response']['items']
            for comm in comments:
                if comm['likes']['count'] >= config.LIKES_TO_BE_IN_ANSWERS or comm['likes']['user_likes'] == 1:
                    text_to_append = text_utils.remove_links(comm['text'])
                    if comm.get('attachments'):
                        for el in comm['attachments']:
                            text_to_append += config.SPLIT_SIGN + unicode(el['type']) + \
                                            unicode(el[el['type']]['owner_id']) + u'_' + unicode(el[el['type']]['id'])
                    public[-1]['answers'].append(text_to_append)


        cur += len(posts)
    #for post in public:
    #    print post
    return public

def limit_answer(string):
    message_length = config.MAX_MESSAGE_LENGTH
    if len(string) < message_length:
        return string
    else:
        i = len(string) - 1
        while string[i] != u' ' or i > message_length:
            i -= 1
        return string[:i] + '...'

def get_users(uids):
    if not isinstance(uids, list):
        if isinstance(uids, int) or isinstance(uids, str) or isinstance(uids, unicode):
            uids = [uids]
        else:
            logger.error(u'В функцию получения информации передали не строку и не число. ')
            return False
    users = cdb.users
    unknown_uids = []
    answer = []
    for uid in uids:
        user = users.find_one({'id': int(uid)})
        if int(uid) < 0:
            answer.append({'id': int(uid), 'money': 0, 'first_name': u'', \
                        'last_name': u'', 'domain': u'', 'sex': 2})
            continue
        if user is None:
            unknown_uids.append(str(uid))
            answer.append(int(uid))
        else:
            answer.append(user)
    if len(unknown_uids) == 0:
        return answer
    pars = {
            'user_ids': u','.join(unknown_uids),
            'lang': u'ru',
            'fields': u'domain, sex',
        }
    r = api.query(u'users.get', pars)
    time.sleep(0.4)
    if r is None or r.get('error'):
        err = u'Ошибка во время получения информации о пользователях. '
        if r is not None and r.get('error'):
            err += unicode(r['error'])
        logger.error(err)
        if r is not None and r.get('error').get('error_code') == 6:
            time.sleep(2);
            r = api.query(u'users.get', pars)
        else:
            return False
    info = r['response']
    merged_answer = []
    if len(info) > 0:
        users = cdb.users
        for user in answer:
            if isinstance(user, int):
                ok = False
                for el in info:
                    if int(el['id']) == user:
                        el['money'] = 0
                        users.save(el)
                        merged_answer.append(el)
                        ok = True
                        break
                if not ok:
                    merged_answer.append({'id': user, 'money': 0, 'first_name': u'', \
                        'last_name': u'', 'domain': u'', 'sex': 2})
            else:
                merged_answer.append(user)
        return merged_answer
    else:
        return answer

def get_bot_info(name=None):
    if name is not None:
        bot = cdb.bots.find_one({'name': name})
    else:
        try:
            bot_name = config.BOT_NAME
        except:
            logger.log(u'Обращение к информации о боте без правильного configа.')
            return None
        bot = cdb.bots.find_one({'name': config.BOT_NAME})
    return bot

def set_bot_status(info, status, sid=0):
    if status == 'ok':
        if info['status'] != 'ok':
            cdb.captcha_queue.remove({'id': info['id']})
        info['status'] = status
        info['sid'] = sid
        info['lost_requests'] = 0
        cdb.bots.save(info)
        return info
    elif status == 'error': 
        if info['status'] == 'error':
            info['lost_requests'] += 1
        else:
            info['status'] = status
            info['lost_requests'] = 1
            info['sid'] = sid
            cdb.captcha_queue.insert({
                'id': info['id'], 
                'name': info['name'],
                'sid': sid })
        cdb.bots.save(info)
        return info
