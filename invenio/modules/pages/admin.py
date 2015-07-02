# -*- coding: utf-8 -*-
# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Pages module admin views."""

from flask import current_app

from invenio.base.globals import cfg
from invenio.ext.admin.views import ModelView
from invenio.ext.sqlalchemy import db
from invenio.modules.pages.models import Page, PageList

from jinja2 import TemplateNotFound

from werkzeug.local import LocalProxy

from wtforms import IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


def template_exists(form, field):
    """Check selected template existance."""
    try:
        current_app.jinja_env.get_template(field.data)
    except TemplateNotFound:
        raise ValidationError("Selected template does not exist.")


def same_page_choosen(form, field):
    """Check that we are not trying to assign list page itself as a child."""
    if form._obj is not None:
        if field.data.id == form._obj.list_id:
            raise ValidationError(
                'You cannot assign list page itself as a child.')


class PagesAdmin(ModelView):
    """Page model admin view."""
    _can_create = True
    _can_edit = True
    _can_delete = True

    create_template = 'pages/edit.html'
    edit_template = 'pages/edit.html'

    column_list = (
        'url', 'title', 'last_modified',
    )
    column_searchable_list = ('url',)
    column_labels = dict(url='URL')

    page_size = 100

    form_excluded_columns = ('lists')
    form_args = dict(
        template_name=dict(
            default=LocalProxy(
                lambda: cfg["PAGES_DEFAULT_TEMPLATE"]),
            description=LocalProxy(
                lambda: "Default: %s" % cfg["PAGES_DEFAULT_TEMPLATE"]),
            validators=[DataRequired(), template_exists]
        ),
    )
    form_widget_args = {
        'created': {
            'style': 'pointer-events: none;',
            'readonly': True
        },
        'last_modified': {
            'style': 'pointer-events: none;',
            'readonly': True
        },
    }
    form_overrides = dict(content=TextAreaField, description=TextAreaField)

    inline_models = [
        (PageList, {
            'form_columns': ['id', 'order', 'page'],
            'form_overrides': {'order': IntegerField},
            'form_args': {'page': {'validators': [same_page_choosen]}}
        })
    ]

    def __init__(self, model, session, **kwargs):
        """Initialize PagesAdmin."""
        super(PagesAdmin, self).__init__(
            model, session, **kwargs
        )


def register_admin(app, admin):
    """Called on app initialization to register administration interface."""
    admin.add_view(PagesAdmin(
        Page, db.session,
        name='Pages',
        category='')
    )
