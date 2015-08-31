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
from markupsafe import Markup

from flask import flash, render_template
from flask_admin.actions import action
from flask_admin.form.fields import DateTimeField
from flask_admin.model.form import InlineFormAdmin

from invenio.ext.admin.views import ModelView
from invenio.ext.sqlalchemy import db

from invenio.ext.login import login_user, logout_user

from invenio.modules.workflows.models import BibWorkflowObject, Workflow, ObjectVersion
from invenio.modules.workflows.engine import WorkflowStatus


from .models import Deposition

class AccMixin(object):

    """Configure access rights."""

    _can_create = False
    _can_edit = False
    _can_delete = False

    acc_view_action = 'cfgwebaccess'
    acc_edit_action = 'cfgwebaccess'
    acc_delete_action = 'cfgwebaccess'


def name_from_workflowstatus(s):
    if s == WorkflowStatus.NEW:
        return "NEW"
    elif s == WorkflowStatus.RUNNING:
        return "RUNNING"
    elif s == WorkflowStatus.HALTED:
        return "HALTED"
    elif s == WorkflowStatus.ERROR:
        return "ERROR"
    elif s == WorkflowStatus.COMPLETED:
        return "COMPLETED"


def format_deposition(v, c, m, n):
    """Format data for a deposition."""
    return Markup(render_template(
        "deposit/admin/deposition_data.html", obj=Deposition(m)))


class DepositAdmin(ModelView, AccMixin):

    """Flask-Admin view to manage users."""

    can_view_details = True

    column_list = (
        'id', 'user', 'id_workflow', 'version', 'workflow.status', 'created',
        'modified',
    )

    column_details_list = (
        'id',
        'user',
        'version',
        'workflow.status',
        'created',
        'modified',
        '_data',
        'child_logs',
    )

    column_names = {
        '_data': 'Data',
    }

    column_filters = (
        'user.email',
        'user.nickname',
        'created',
        'modified',
    )

    column_formatters = {
        'version': lambda v, c, m, n: ObjectVersion.name_from_version(
            getattr(m, n)),
        'workflow.status': lambda v, c, m, n: name_from_workflowstatus(
            m.workflow.status),
        '_data': format_deposition
    }

    def get_query(self):
        params = [
            Workflow.module_name == 'webdeposit',
            BibWorkflowObject.id_user != 0
        ]

        return BibWorkflowObject.query.join("workflow").options(
            db.contains_eager('workflow')).filter(*params)


def register_admin(app, admin):
    """Call on app initialization to register administration interface."""
    category = "Deposits"
    admin.add_view(DepositAdmin(
        BibWorkflowObject, db.session, name="Deposits", category=category
    ))
