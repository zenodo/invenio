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

from invenio.ext.sqlalchemy import db
from invenio.modules.upgrader.api import op


depends_on = [u'pages_2014_04_22_new_model']


def info():
    """Short description."""
    return "Providing pages list."


def do_upgrade():
    """Upgrades."""
    op.add_column(u'pages', db.Column('description', db.String(length=200),
                                      nullable=True))
    op.create_table(
        'pagesLIST',
        db.Column('id', db.Integer(15, unsigned=True), nullable=False),
        db.Column('list_id', db.Integer(15, unsigned=True), nullable=False),
        db.Column('page_id', db.Integer(15, unsigned=True), nullable=False),
        db.Column('order', db.Integer(15, unsigned=True), nullable=False),
        db.PrimaryKeyConstraint('id'),
        db.ForeignKeyConstraint(['list_id'], [u'pages.id'], ),
        db.ForeignKeyConstraint(['page_id'], [u'pages.id'], ),
        mysql_charset='utf8',
        mysql_engine='MyISAM'
    )


def estimate():
    """Estimate running time of upgrade in seconds (optional)."""
    return 1
