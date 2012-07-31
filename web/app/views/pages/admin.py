# -*- coding: utf-8 -*-

import datetime
from werkzeug.datastructures import ImmutableMultiDict
from flask import g, Blueprint, render_template, request
from settings import PAGES
from forms import PageForm

bp = Blueprint(
    'admin_pages',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/admin/pages/'
)

#~ view functions
def list_pages():
    context = {}
    context['pages'] = g.db.db.pages.find({})

    return render_template('pages/list.html', **context)

def add():
    context = {}
    context['form'] = form = PageForm()
    form.author.data = 'Ich'

    print dir(bp)

    if form.validate_on_submit():
        pages = g.db.db.pages
        result = pages.insert(form.data)

        context['success'] = True

    return render_template('pages/add.html', **context)

def edit(page_slug):
    context = {}
    pages = g.db.db.pages
    context['page'] = page = pages.find_one_or_404({'slug': page_slug})
    context['form'] = form = PageForm(request.form, **page)

    if form.validate_on_submit():
        print form.data
        result = pages.update({'slug': page_slug}, form.data)

        print result

        context['success'] = True

    return render_template('pages/edit.html', **context)

def delete(page_slug):
    context = {}
    context['success'] = False
    pages = g.db.db.pages
    result = pages.remove({'slug': page_slug})

    if result['n'] >= 1: context['success'] = True

    return render_template('pages/del.html', **context)

#~ define urls
bp.add_url_rule('delete/<page_slug>/', methods=('GET', 'POST'), view_func=delete)
bp.add_url_rule('<page_slug>/', methods=('GET', 'POST'), view_func=   edit)
bp.add_url_rule('add/', methods=('GET', 'POST'), view_func=add)
bp.add_url_rule('', view_func=list_pages)