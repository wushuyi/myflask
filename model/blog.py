# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from . import db

posts_classifys = db.Table(
    'blog_posts_classify',
    db.Column('id', db.Integer(), primary_key=True),
    db.Column('post_id', db.Integer(), db.ForeignKey('blog_post.id')),
    db.Column('classify_id', db.Integer(), db.ForeignKey('blog_classify.id')),
)


class BlogPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    uri_path = db.Column(db.String(255))
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    markdown = db.Column(db.Text())
    pre_content = db.Column(db.Text())
    pre_markdown = db.Column(db.Text())
    classify = db.relationship(
        'BlogClassify', secondary=posts_classifys,
        backref=db.backref('blogposts', lazy='dynamic')
    )

    def __str__(self):
        return self.title


class BlogClassify(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    uri_path = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __str__(self):
        return self.name
