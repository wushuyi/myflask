# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask.ext.script import Manager
from myapp import app

manager = Manager(app)


@manager.command
def drop_db():
    from model.create_db import db

    db.init_app(app)
    db.drop_all()


@manager.command
def init_db():
    import string
    import random
    from flask.ext.security.utils import encrypt_password
    from model.create_db import db
    from model.security import User, Role
    from controllers.security import user_datastore, security

    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    security.init_app(app)
    db.drop_all()
    db.create_all()

    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    user_datastore.create_user(
        first_name='Admin',
        email='admin',
        password=encrypt_password('admin'),
        roles=[user_role, super_user_role]
    )

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie', 'Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]

    for i in range(len(first_names)):
        tmp_email = first_names[i].lower() + "." + last_names[i].lower() + "@example.com"
        tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
        user_datastore.create_user(
            first_name=first_names[i],
            last_name=last_names[i],
            email=tmp_email,
            password=encrypt_password(tmp_pass),
            roles=[user_role, ]
        )
    db.session.commit()


@manager.command
def init_blog_db():
    from model.create_db import db
    import model.blog

    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    manager.run()
