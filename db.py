#!/usr/bin/python
from pymongo import MongoClient
import config
c = MongoClient()
db = c[config.BOT_NAME + '_database']

