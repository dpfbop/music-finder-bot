#!/usr/bin/python
# -*- coding: utf-8 -*-
BOT_NAME = 'your_name'



BOT_ID = #vk id
BOT_ENABLED = True #
BOT_TOKEN = u'' #access_token
BOT_NAMES = [u'music', u'bot', u'finder', u'музон', u'бот']
BOT_PRIORITY = 3
BOT_LEARN_PUBLIC = -73268019

ROOT = '/var/bot_project/'
RESOURCES = ROOT + 'resources/'
BOT_FOLDER = ROOT + 'music_finder_bots/' + BOT_NAME + '/'
ERROR_FILE = BOT_FOLDER + 'logs/err.log'
LOG_FILE = BOT_FOLDER + 'logs/log.log'

SLEEP_SERVER_FALL = 6 / BOT_PRIORITY
SLEEP_VK_NO_RESPONSE = 5 / BOT_PRIORITY
SLEEP_BETWEEN_REQUESTS = 3 / BOT_PRIORITY

ADMIN_IDS = [17890829, 8734581, 231219001]
LANA_TOKEN = u'1a72d5045bbf8657be283858a96bb55773f8bbab3a0cd827ac43de83'
MAIN_LEARN_PUBLIC = -73268019
NUMBER_MESSAGES = 10
DIALOG_LENGTH = 10
TIME_TO_MARK_AS_READ = 5  #seconds

DOMAINS_FILE = RESOURCES + 'domains.txt'
MUSIC_ID = 6027233
GALLOWS_WORDS = RESOURCES + 'words.txt'
GALLOWS_LIFES = 7
NUMBER_OF_NEWS = 5
MAX_MESSAGE_LENGTH = 500
DAYS_BEFORE_LEAVING_THE_DIALOG = 10
LIKES_TO_BE_IN_ANSWERS = 5
SPLIT_SIGN = u'$&$&$'
NUMBER_OF_USERS_IN_RICHEST_POST = 3
