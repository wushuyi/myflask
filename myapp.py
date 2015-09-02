# -*- coding: utf-8 -*-
from flask import Flask
import config
from flask_kvsession import KVSessionExtension
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore
from model.link_redis import strictredis

app = Flask(__name__)
app.config.from_object(config)

store = RedisStore(strictredis)
prefixed_store = PrefixDecorator('sessions_', store)
KVSessionExtension(prefixed_store, app)


def register_all():
    import controllers.security
    import controllers.admin
    import controllers.babel

    controllers.security.register(app)
    controllers.admin.register(app)
    controllers.babel.register(app)


if __name__ == '__main__':
    register_all()
    app.run(host='0.0.0.0', port=5000)
