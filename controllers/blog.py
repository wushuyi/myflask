# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
import os
from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from model import db
from model.blog import BlogPost, BlogClassify
from model.security import User


blog_page = Blueprint(
    'blog_page ',
    __name__,
    template_folder='templates'
)


@blog_page.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=301)


@blog_page.route('/')
def home():
    post_list = BlogPost.query.limit(10).all()
    classify_list = BlogClassify.query.all()
    return render_template('blog/index.html', post_list=post_list, classify_list=classify_list)


@blog_page.route('/posts/<query_path>')
def posts(query_path):
    post = BlogPost.query.filter_by(uri_path=query_path).first_or_404()
    return render_template('blog/posts.html', post=post)

@blog_page.route('/tag/<query_classify>')
def tag(query_classify):
    return query_classify

def register(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if not hasattr(app.extensions, 'sqlalchemy'):
        db.init_app(app)
    app.register_blueprint(blog_page)

    @app.context_processor
    def add_context():
        return {
            'site_title': app.config['SIET_TITLE']
        }