#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
from random import choice

class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Ванга', True, False, \
                                u'Это знаменитый шар предсказаний &#127921; <br> Он сможет ответить на любой вопрос.',\
                                [u'правда, что я - лучший?',])
        self.dialog = dialog

    def run(self):
        args = self.dialog.last_message.args
        request = ''.join([el.lower() for el in args])
        dic = [u'Бесспорно.',
               u'А как же иначе?',
               u'Абсолютно точно!',
               u'Думаю да.',
               u'Отрицательно',
               #u'Предрешено.',
               u'Никаких сомнений.',
               #u'Определённо да.',
               u'Конечно нет.',
               u'Можешь быть уверен в этом.',
               u'Мне кажется — «да».',
               u'Вероятнее всего.',
               u'Хорошие перспективы.',
               u'Знаки говорят — «да».',
               u'Да.',
               u'Лучше не рассказывать.',
               u'Не знаю.',
               u'Даже не думай.',
               u'Мой ответ — «нет».',
               u'Перспективы не очень хорошие.',
               u'Весьма сомнительно.',
               u'Скорее всего нет.',
               u'Что-то мне подсказывает, что нет.',
               u'Естественно нет.']
        if len(request) <= 5:
            string = choice(dic)
        else:
            string = dic[int(hash(request)) % len(dic)]
        string = u'&#127921; ' + string
        return self.dialog.answer(unicode(string))
