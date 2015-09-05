# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask import current_app, abort
from flask import Blueprint, render_template, redirect, url_for
from model import db
from model.blog import BlogPost, BlogClassify
import math
import view.blog as blog

blog_page = Blueprint(
    'blog_page ',
    __name__,
    template_folder='templates'
)

blog_page.add_app_template_global(blog.get_public, name='blog_public')
blog_page.add_app_template_global(blog.get_classify_list, name='blog_get_classify_list')

blog_page.add_url_rule('/favicon.ico', endpoint='page', view_func=blog.favicon)
blog_page.add_url_rule('/list/<int:page>', endpoint='post_list', view_func=blog.post_list)
blog_page.add_url_rule('/', endpoint='home', view_func=blog.post_list)

blog_page.add_url_rule('/tag/<string:query_classify>/<int:page>', endpoint='tag_list', view_func=blog.tag_list)
blog_page.add_url_rule('/tag/<string:query_classify>', endpoint='tag', view_func=blog.tag_list)

blog_page.add_url_rule('/article/<string:query_path>', endpoint='posts', view_func=blog.posts)

blog_page.add_url_rule('/search', endpoint='search', view_func=blog.search)
blog_page.add_url_rule('/search/<int:page>', endpoint='search_list', view_func=blog.search)


def register(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if not hasattr(app.extensions, 'sqlalchemy'):
        db.init_app(app)
    app.register_blueprint(blog_page)
