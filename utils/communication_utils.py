#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Template
import random
from datetime import datetime, timedelta
from db import *
from common_db import cdb
import time
from utils import text_utils
from smiles import smiles
import random
import config

questions = []
if config.MAIN_LEARN_PUBLIC == config.BOT_LEARN_PUBLIC:
    questions = list(cdb.communication.find())
else:
    questions = list(db.communication.find())


def translate_irisscript(q):
    q = text_utils.remove_links(q)
    now = datetime.now()
    variables = {
        'mood': 6,
        'year': now.year,
        'month': now.month,
        'day': now.day, 
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'random': random.randint(0, 1000),
    }
    pref = u'varss.'
    relations = {
        u'настроение': pref + u'mood',
        u'год': pref + u'year',
        u'месяц': pref + u'month',
        u'день': pref + u'day',
        u'час': pref + u'hour',
        u'минута': pref + u'minute',
        u'секунда': pref + u'second',
        u'рандом': pref + u'random',
        u'если': u'if',
        u'все': u'endif',
        u'если_иначе': u'elif',
        u'иначе': u'else',
        u'напиши': u'write',
        u'и': u'and',
        u'или': u'or',
        u'больше': u'>',
        u'меньше': u'<',
        u'меньше_равно': u'>=',
        u'больше_равно': u'<=',
        u'равно': u'==',
        u'не_равно': u'!=',
        u'равен': u'==',

    }
    t = u''
    last_pos = 0
    while 1:
        start = q.find(u'{', last_pos)
        if start == -1:
            break
        t += q[last_pos:start]
        end = q.find(u'}', last_pos)
        last_pos = end + 1
        commands = q[start + 1:end].split()  
        commands = [el.lower() for el in commands]
        for i in xrange(len(commands)):
            for el in relations:
                if el == commands[i]:
                    commands[i] = relations[el]
                    break
        if len(commands) == 2 and commands[0] == u'write':
            t += u'{{ ' + commands[1] + u' }}'    
        else:
            t += u'{% ' + u' '.join(commands) + u' %}'    

    t += q[last_pos:]
    #print t
    template = Template(t)
    ans = template.render(varss = variables)
    if len(ans.strip()) == 0:
        return None
    else:
        return ans

def find_answer(question):
    question = text_utils.remove_extra_symbols(question)
    used = set()
    def crawl(question):
        mindist = float('Inf')
        query = None
        global questions
        for q in questions:
            if q['id'] in used:
                continue
            variations = [q['question']] + q['same_as']
            for el in variations:
                tmp = text_utils.levenstein_dist(el, question) 
                if tmp < mindist:
                    mindist = tmp
                    query = q
        if float(mindist) / (len(unicode(question)) + 1) <= 0.2:
            used.add(query['id'])
            print used
            answers = query['answers']
            if query.get('same_as') and len(query['same_as']) > 0:
                for same_question in query['same_as']:
                    answers += crawl(same_question)
            return answers
        else:
            return []
    answers = crawl(question)
    if len(answers) == 0:
        return damn()
    rand_ans = random.randint(0, len(answers) - 1)
    for ans in answers[rand_ans:] + answers[0:rand_ans]:
        tmp = translate_irisscript(ans)
        if tmp is not None:
            return tmp
    return damn()

def damn():
    dic = [u'Очень сложно &#128528;<br>',
            u'Не понимаю &#128513;<br>',
            #u'Я очень устала &#128531;<br>', 
            u'Лучше спроси, что я делаю :)<br>',
            u'Лучше спроси, как дела.<br>',
            #u'Лучше репостни мою группу ' + smiles['xD'] + u'<br>',
            u'Попробуй функцию анонимно ' + smiles['wink'] + u'<br>',
            u'Попробуй функцию новости ' + smiles['peace'] + u'<br>',
            u'Поиграй в виселицу ' + smiles['smile'] + u'<br>',
            u'Попробуй функцию вики' + smiles['wink'] + u'<br>',
            u'Сыграй со мной в одну игру ' + smiles['devil'] + u'<br>',
            u'Добавь меня в чат с друзьями ' + smiles['xD'] + u'<br>',
            u'Я пока не могу ответить на этот вопрос. <br>' + \
                u'Посоветуй интересные вопросы для Ирис через "предложить новость" в паблике Обучение Ирис :)<br>',
          ]
    string = unicode(random.choice(dic))
    string += u'Команда "помощь" - список доступных команд. <br>'
    return string
