# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
import redis
import config

strictredis = redis.StrictRedis(
    host=config.REDIS_HOST,
    password=config.REDIS_PASSWORD,
    port=config.REDIS_PORT,
    db=config.REDIS_DB
)
