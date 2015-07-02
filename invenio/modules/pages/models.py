# -*- coding: utf-8 -*-
#
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

"""Pages module models."""

from datetime import datetime

from invenio.ext.sqlalchemy import db


class Page(db.Model):
    """Represents a page."""
    __tablename__ = 'pages'

    id = db.Column(db.Integer(15, unsigned=True), nullable=False,
                   primary_key=True, autoincrement=True)
    """Page identifier."""

    url = db.Column(db.String(100), unique=True, nullable=False)
    """Page url."""

    title = db.Column(db.String(200), nullable=True)
    """Page title."""

    content = db.Column(
        db.Text().with_variant(db.Text(length=2**32-2), 'mysql'),
        nullable=True)
    """Page content. Default is pages/templates/default.html"""

    description = db.Column(db.String(200), nullable=True)
    """Page description."""

    template_name = db.Column(db.String(70), nullable=True)
    """Page template name. Default is cfg["PAGES_DEFAULT_TEMPLATE"]."""

    created = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    """Page creation date."""

    last_modified = db.Column(db.DateTime(), nullable=False,
                              default=datetime.now, onupdate=datetime.now)
    """Page last modification date."""

    def __repr__(self):
        """Page representation.

        Used on Page admin view in inline model.

        :returns: unambiguous page representation.
        """
        return "URL: %s, title: %s" % (self.url, self.title)


class PageList(db.Model):
    """Represent association between page and list."""
    __tablename__ = 'pagesLIST'

    id = db.Column(db.Integer(15, unsigned=True), nullable=False,
                   primary_key=True, autoincrement=True)
    """PageList identifier."""

    list_id = db.Column(db.Integer(15, unsigned=True),
                        db.ForeignKey(Page.id), nullable=False)
    """Id of a list."""

    page_id = db.Column(db.Integer(15, unsigned=True),
                        db.ForeignKey(Page.id), nullable=False)
    """Id of a page."""

    order = db.Column(db.Integer(15, unsigned=True), nullable=False)

    list = db.relationship(Page,
                           backref=db.backref("pages",
                                              cascade="all, delete-orphan"),
                           foreign_keys=[list_id])
    """Relation to the list."""

    page = db.relationship(Page,
                           backref=db.backref("lists",
                                              cascade="all, delete-orphan"),
                           foreign_keys=[page_id])
    """Relation to the page."""


__all__ = ['Page', 'PageList']
