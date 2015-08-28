# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Flask-Admin page to configure users and accounts."""

from __future__ import absolute_import

from flask import flash
from flask_admin.actions import action
from flask_admin.form.fields import DateTimeField
from flask_admin.model.form import InlineFormAdmin

from invenio.ext.admin.views import ModelView
from invenio.ext.sqlalchemy import db

from invenio.ext.login import login_user, logout_user

from .models import User, UserEXT


class AccMixin(object):

    """Configure access rights."""

    _can_create = True
    _can_edit = True
    _can_delete = False

    acc_view_action = 'cfgwebaccess'
    acc_edit_action = 'cfgwebaccess'
    acc_delete_action = 'cfgwebaccess'


class UserEXTInlineModelForm(InlineFormAdmin):

    """Inline admin for UserEXT."""
    form_columns = ('method', 'id')


class UserAdmin(ModelView, AccMixin):

    """Flask-Admin view to manage users."""

    column_list = (
        'id', 'nickname', 'email', 'family_name', 'given_names',
        'note', 'last_login', 'password_scheme',
    )

    form_columns = (
        'nickname', 'email', 'family_name', 'given_names',
        'note', 'last_login', 'password_scheme',
    )

    column_searchable_list = (
        'nickname', 'email', 'family_name', 'given_names', 'password_scheme',
    )

    column_filters = (
        'note', 'password_scheme'
    )

    form_overrides = {
        'last_login': DateTimeField
    }

    inline_models = [UserEXTInlineModelForm(UserEXT)]

    @action('inactivate', 'Inactivate',
            'Are you sure you want to inactivate selected users?')
    def action_inactivate(self, ids):
        """Inactivate users."""
        try:
            query = User.query.filter(User.id.in_(ids))
            count = 0
            for user in query.all():
                if user.inactivate():
                    count += 1

            if count > 0:
                flash('User(s) were successfully inactivated.', 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash('Failed to inactivate users. %(error)s' %
                  dict(error=str(ex)),
                  'error')

    @action('activate', 'Activate',
            'Are you sure you want to activate selected users?')
    def action_activate(self, ids):
        """Inactivate users."""
        try:
            query = User.query.filter(User.id.in_(ids))
            count = 0
            for user in query.all():
                if user.activate():
                    count += 1

            if count > 0:
                flash('User(s) were successfully inactivated.', 'success')
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash('Failed to inactivate users. %(error)s' %
                  dict(error=str(ex)),
                  'error')

    @action('become_user', 'Become user')
    def action_become_user(self, ids):
        """Inactivate users."""
        try:
            if len(ids) != 1:
                flash('You can only become one user at a time.', '')
            user = User.query.get(ids[0])
            logout_user()
            login_user(user)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash('Failed to become users. %(error)s' %
                  dict(error=str(ex)),
                  'error')


def register_admin(app, admin):
    """Call on app initialization to register administration interface."""
    category = "Accounts"
    admin.add_view(
        UserAdmin(User, db.session, name="Users", category=category)
    )
