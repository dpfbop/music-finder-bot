#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import traceback
import config
from utils import api
from classes import *
import pdb
import math
from collections import deque
import cProfile
#from utils import communication_utils


def sleep_enough():  #возврашает время с последнего запроса И Спит
    global last_req_time
    elapsed = time.time() - last_req_time
    time_difference = config.SLEEP_BETWEEN_REQUESTS - elapsed
    if time_difference >= 0:
        time.sleep(time_difference)
    elapsed = time.time() - last_req_time
    last_req_time = time.time()
    return elapsed

MESSAGES_RESPONDED = deque([0 for i in xrange(config.NUMBER_MESSAGES)])


def cut_messages_responded():
    global messages_responded
    l = max(0, len(messages_responded) - 2 * config.NUMBER_MESSAGES)
    messages_responded = messages_responded[l:]


last_req_time = time.time()
def main(from_shell=False):
    bot = Bot()
    if from_shell:
        print u'Bot ' + unicode(bot.name) + u' is running!'
    while True:
        try:
            time_offset = math.ceil(sleep_enough())
            response = api.query('messages.get',\
                                 {'count': unicode(config.NUMBER_MESSAGES),
                                 'time_offset': unicode(time_offset)}, 
                                 bot=bot)

            if response is None or response.get('response') is None:
                sleep_time = config.SLEEP_SERVER_FALL if response is None else config.SLEEP_VK_NO_RESPONSE
                time.sleep(sleep_time)
                print response.get('error')
                continue

            messages = response['response']
            messages = messages['items'][::-1]

            for mess in messages:
                message = Message(mess, bot)
                if message.is_mine():
                    if message.id not in MESSAGES_RESPONDED:
                        message.mark_as_read()
                        message.identify_command()
                        dialog = Dialog(message)
                        sleep_enough()
                        successful = dialog.run()
                        if successful:
                            MESSAGES_RESPONDED.append(message.id)
                            MESSAGES_RESPONDED.popleft()
                else:
                    del message

        except Exception as e:
            if from_shell:
                print traceback.format_exc()
            try:
                logger.error(traceback.format_exc())
            except:
                logger.error(u'Mistake in except, lololol.')
            continue

if __name__ == "__main__":
    main(True)
