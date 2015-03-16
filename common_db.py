#!/usr/bin/python
from pymongo import MongoClient
c = MongoClient()
cdb = c.common_database_for_bots
