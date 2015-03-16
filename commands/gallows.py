#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate

from db import *
import codecs
import config
import random
import logger
from smiles import smiles
from utils import vk_utils


class Command(CommandTemplate, object):

    def __init__(self, dialog):
        CommandTemplate.__init__(
            self, u'Виселица',
            True, False,
            u'Игра в виселицу. Для начала напишите "виселица старт" и угадывайте буквы."' +
            config.BOT_NAMES[0] +
            u' вис рейтинг" покажет список из 10 лучших игроков. ',
            [u'виселица старт', u'вис а', u'вис н']
        )
        self.dialog = dialog

    def run(self):
        gallows_games = db.gallows_games

        def in_alph(letter):
            if len(letter) != 1:
                return False
            big = ord(u'А') <= ord(unicode(letter)) <= ord(u'Я')
            small = ord(u'а') <= ord(unicode(letter)) <= ord(u'я')
            return small or big

        dialog = self.dialog
        args = dialog.last_message.args
        if len(args) < 1 or args[0] is None:
            return dialog.answer(u'Введите "' + config.BOT_NAMES[0] + u' виселица старт" для начала или "' +
                                 config.BOT_NAMES[0] + u' вис [буква]"')
        request = unicode(args[0])
        dialog_id = dialog.dialog_id
        f = codecs.open(config.GALLOWS_WORDS, mode='r', encoding='utf-8')
        if request == u'рейтинг':
            def pictilize(string):
                return smiles['transform_letter'].join(str(string)) + smiles['transform_letter']
            winners = [winner for winner in db.gallows_rating.find()]
            if len(winners) == 0:
                return dialog.answer(u'Пока никто не выиграл в виселицу. :(')
            winners = sorted(
                winners, key=lambda player: player['score'], reverse=True)
            you = False
            pos = -1
            for i in xrange(len(winners)):
                if winners[i]['uid'] == dialog.last_message.user_id:
                    you = winners[i]
                    pos = i

            top = [unicode(winner['first_name']) + u' ' +
                   unicode(winner['last_name'] + u': ' +
                           pictilize(winner['score'])) for winner in winners[:10]]
            top[0] += u' ' + smiles['goblet']
            for i in xrange(len(top)):
                top[i] = unicode(str(i + 1)) + u'. ' + top[i]
            if pos == -1 or pos > 10:
                if pos != -1:
                    top.append(
                        unicode(str(pos + 1)) + u'. 'u'Вы: ' + pictilize(you['score']))
            return dialog.answer(u'<br>'.join(top))
        if request != u'старт' and gallows_games.find_one({u'dialog_id': dialog_id}) is None:
            return dialog.answer(u'Сначала начните игру.\nДля этого введите "' + unicode(config.BOT_NAMES[0]) + u' вис старт".')
        if request == u'старт':
            if gallows_games.find_one({u'dialog_id': dialog_id}) is not None:
                return dialog.answer(u"Игра уже идет\n")
            s = u''
            c = []
            for i in xrange(random.randrange(0, 64000)):
                s = f.readline()
            while len(s) <= 3 or s[-2] == '.':
                s = f.readline()
            f.close()
            ss = s[:-1].upper()
            for i in xrange(len(ss)):
                c.append(u'__ ')
            game = {
                u'dialog_id': dialog_id,
                u'word': unicode(ss),
                u'lifes': config.GALLOWS_LIFES,
                u'guessed': c,
                u'used': ['']
            }
            gallows_games.save(game)
            print game
            return dialog.answer(unicode(u''.join(c)) + "\n")
        elif in_alph(request):  # request.lower() in alph.keys():
            if gallows_games.find_one({u'dialog_id': dialog_id}) is None:
                return dialog.answer("Сначала начните игру\n")
            request = request.upper()
            game = gallows_games.find_one({u'dialog_id': dialog_id})
            request = unicode(request)
            if request in game[u'used']:
                return dialog.answer(u'Букву ' + unicode(request) + u" уже называли &#128528;\n")
            game[u'used'].append(request)
            if request in game[u'word']:
                c = game[u'guessed']
                for i in xrange(len(game[u'word'])):
                    if game[u'word'][i] == request:
                        c[i] = u' ' + request + u'  '
                game[u'guessed'] = c
                print game[u'guessed']
                if u'__ ' not in game[u'guessed']:
                    ans = game[u'guessed']
                    gallows_games.remove({u'dialog_id': dialog_id})
                    ans = u''.join(ans)
                    ans = ans.replace(u' ', u'')
                    rating = db.gallows_rating
                    winner = rating.find_one(
                        {u'uid': dialog.last_message.user_id})
                    if not winner:
                        winner = {
                            u'uid': dialog.last_message.user_id,
                            u'first_name': u'',
                            u'last_name': u'',
                            u'score': 0,
                        }
                        info = vk_utils.get_users(
                            [dialog.last_message.user_id])
                        if not info or len(info) == 0:
                            return dialog.answer(u'Правильно! Вы выиграли, но ваш результат не был сохранен. ')
                        info = info[0]
                        winner['first_name'] = info['first_name']
                        winner['last_name'] = info['last_name']
                    winner['score'] += 1
                    rating.save(winner)
                    return dialog.answer(u"Правильно!\n" + unicode(ans) + u"\nВы выиграли!!!\n")
                else:
                    gallows_games.save(game)
                    ans = u''
                    for i in xrange(len(game[u'guessed'])):
                        ans += game[u'guessed'][i]
                    return dialog.answer(u"Правильно! В слове есть буква " + request.upper() +
                                         ".\n" + unicode(ans) + u"\n")
            else:
                game[u'lifes'] = game[u'lifes'] - 1
                if game[u'lifes'] == 0:
                    ans = game[u'word']
                    gallows_games.remove({u'dialog_id': dialog_id})
                    return dialog.answer(u"Вы проиграли! Загаданное слово - " + u''.join(ans) + u"\n")
                else:
                    gallows_games.save(game)
                    return dialog.answer(u"Ой-ой, буквы " + request.upper() + u" нет. Минус жизнь. Осталось: <br>" +
                                         u"&#10084; " * game[u'lifes'] + u"&#128148; " * (config.GALLOWS_LIFES - game[u'lifes']) + "\n")
        else:
            return dialog.answer(u'Введите одну русскую букву')
