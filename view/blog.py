# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask import current_app, abort, request
from flask import Blueprint, render_template, redirect, url_for
from model import db
from model.blog import BlogPost, BlogClassify
import math


def favicon():
    return redirect(url_for('static', filename='favicon.ico'), code=301)


def get_public():
    app = current_app._get_current_object()
    return {
        'title': app.config['SIET_TITLE'],
    }


def get_classify_list():
    classify_list = BlogClassify.query.all()
    return classify_list


def post_list(**kwargs):
    page = kwargs.pop("page", 1)
    app = current_app._get_current_object()
    post_max = app.config['SIET_LIST_SIZE']
    post_list = BlogPost.query.order_by(BlogPost.id.desc())[((page - 1) * post_max):(page * post_max)]
    if len(post_list) == 0:
        abort(404)

    post_count = BlogPost.query.count()
    post_page = math.ceil(post_count / post_max)
    page_control = {
        'previous': None,
        'next': None,
    }

    if page != 1:
        page_control['previous'] = url_for('.post_list', page=(page - 1))
        if page == 2:
            page_control['previous'] = url_for('.home')

    if page != post_page:
        page_control['next'] = url_for('.post_list', page=(page + 1))
    return render_template('blog/index.html', post_list=post_list, page_control=page_control)


def tag_list(**kwargs):
    query_classify = kwargs.pop("query_classify", None)
    app = current_app._get_current_object()
    post_max = app.config['SIET_LIST_SIZE']
    page = kwargs.pop("page", 1)
    classify = BlogClassify.query.filter_by(uri_path=query_classify).first_or_404()
    post_list = classify.blogposts.order_by(BlogPost.id.desc())[((page - 1) * post_max):(page * post_max)]
    if len(post_list) == 0:
        abort(404)

    post_count = classify.blogposts.count()
    post_page = math.ceil(post_count / post_max)
    page_control = {
        'previous': None,
        'next': None,
    }
    if page != 1:
        page_control['previous'] = url_for('.tag_list', query_classify=query_classify, page=(page - 1))
        if page == 2:
            page_control['previous'] = url_for('.tag', query_classify=query_classify)
    if page != post_page:
        page_control['next'] = url_for('.tag_list', query_classify=query_classify, page=(page + 1))

    return render_template('blog/tag.html', classify=classify, post_list=post_list, page_control=page_control)


def posts(query_path):
    post = BlogPost.query.filter_by(uri_path=query_path).first_or_404()
    return render_template('blog/posts.html', post=post)


def search(**kwargs):
    word = request.args['word']
    print(word)
    page = kwargs.pop("page", 1)
    print(page)
    app = current_app._get_current_object()
    post_max = app.config['SIET_LIST_SIZE']
    post_list_where = BlogPost.query.order_by(
        BlogPost.id.desc()
    ).filter(
        BlogPost.markdown.contains(word)
    )
    post_list = post_list_where[((page - 1) * post_max):(page * post_max)]

    post_count = post_list_where.count()

    post_page = math.ceil(post_count / post_max)
    page_control = {
        'previous': None,
        'next': None,
    }

    not_find = post_count == 0
    print(not_find)

    if page != 1:
        page_control['previous'] = url_for('.search_list', page=(page - 1)) + '?word=' + word
        if page == 2:
            page_control['previous'] = url_for('.search') + '?word=' + word

    if page != post_page and not not_find:
        page_control['next'] = url_for('.search_list', page=(page + 1)) + '?word=' + word

    info = {
        'word': word,
        'not_find': not_find
    }

    return render_template('blog/search.html', post_list=post_list, page_control=page_control, info=info)
