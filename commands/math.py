#!/usr/bin/python
# -*- coding: utf-8 -*-
from Command import CommandTemplate
from sympy import solve, simplify, Symbol
from smiles import *
class Command(CommandTemplate, object):
    def __init__(self, dialog):
        CommandTemplate.__init__(self, u'Математика', True, False, \
            u'Решает математические выражения. ', \
            [u'реши x^2 - 1', u'реши x^3 + 16', u'реши sin(x) + cos(x) = 0', u'реши x * y = 12'])
        self.dialog = dialog

    def run(self):
        dialog = self.dialog
        args = dialog.last_message.args
        expr = ''.join(args)
        if expr.count(u'=') > 1:
        	return dialog.answer(u'Слишком много знаков равно для одного выражения. ')
        if expr.count(u'=') == 0:
        	expr += '=0'
        expr = expr.replace(u'ctg', u'cot')
        expr = expr.replace(u'tg', u'tan')
        eqsymbol = expr.find(u'=')
        leftpart = expr[0:eqsymbol]
        rightpart = expr[eqsymbol + 1:]
        try:
        	simplification = simplify(leftpart + '- (' + rightpart + ')')
        except:
        	return dialog.answer(u'Ошибка во входном выражении или оно слишком сложное для меня. ')
        simplification = str(simplification)
        stranswer = u'Упрощенный вид: <br>' + unicode(simplification.replace('cot', 'ctg').replace('tan', 'tg')) + \
        	u' = 0 <br> Решения: ' + u'{'        
        symbls = []
        for c in ['x', 'y', 'a', 'b', 'c']:
        	if simplification.find(c) != -1:
        		symbls.append(Symbol(c))
        try:
        	ans = solve(simplification, symbls)
        except Exception as e:
        	return dialog.answer(unicode(e))
        	return dialog.answer(u'Ошибка во входном выражении или оно слишком сложное для меня. ')
        for i in ans:
        	if unicode(i).count('I') == 0:
        		stranswer += unicode(i) + ', '
        stranswer += u'}'
        stranswer = stranswer.replace(u', }', u'}')
        stranswer = stranswer.replace(u'pi', u'π')
        dialog.answer(stranswer)
