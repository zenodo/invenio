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

"""Unit tests for pages list."""

from invenio.base.wrappers import lazy_import
from invenio.ext.sqlalchemy import db
from invenio.testsuite import InvenioTestCase, make_test_suite, run_test_suite

Page = lazy_import('invenio.modules.pages.models:Page')
PageList = lazy_import('invenio.modules.pages.models:PageList')


def createTestPage(id):
    test_page = Page()
    test_page.id = id
    test_page.url = "pages/test%s" % id
    test_page.title = "My test title %s" % id
    test_page.template_name = 'pages/default.html'
    test_page.content = "Testing pages %s" % id

    return test_page


class PagesListTest(InvenioTestCase):

    """Test pages list functionality."""

    def setUp(self):
        Page.query.delete()
        PageList.query.delete()

        self.test_page1 = createTestPage(1)
        self.test_page2 = createTestPage(2)
        self.test_page3 = createTestPage(3)
        self.test_page4 = createTestPage(4)
        self.test_page5 = createTestPage(5)
        self.test_list1 = PageList(id=1, page_id=2, list_id=1, order=1)
        self.test_list2 = PageList(id=2, page_id=3, list_id=1, order=2)

        db.session.add_all([
            self.test_page1,
            self.test_page2,
            self.test_page3,
            self.test_page4,
            self.test_page5,
            self.test_list1,
            self.test_list2,
        ])
        db.session.commit()

    def tearDown(self):
        db.session.delete(self.test_page1)
        db.session.delete(self.test_page2)
        db.session.delete(self.test_page3)
        db.session.delete(self.test_page4)
        db.session.delete(self.test_page5)

        db.session.delete(self.test_list1)
        db.session.delete(self.test_list2)

        db.session.commit()

    def test_all_objects_where_created(self):
        p = Page.query.count()
        pl = PageList.query.count()

        self.assertEqual(p, 5)
        self.assertEqual(pl, 2)

    def test_deleting_pages_belonging_to_no_lists(self):
        db.session.delete(Page.query.filter_by(id=4).one())
        db.session.delete(Page.query.filter_by(id=5).one())
        db.session.commit()

        p = Page.query.count()
        pl = PageList.query.count()

        self.assertEqual(p, 3)
        self.assertEqual(pl, 2)

    def test_deleting_page_belonging_to_a_list(self):
        db.session.delete(Page.query.filter_by(id=2).one())
        db.session.commit()

        p = Page.query.count()
        pl = PageList.query.count()

        self.assertEqual(p, 4)
        self.assertEqual(pl, 1)

    def test_deleting_page_which_is_a_list(self):
        db.session.delete(Page.query.filter_by(id=1).one())
        db.session.commit()

        p = Page.query.count()
        pl = PageList.query.count()

        self.assertEqual(p, 4)
        self.assertEqual(pl, 0)

    def test_deleting_pagelist_doesnt_affect_page(self):
        db.session.delete(PageList.query.filter_by(id=1).one())
        db.session.delete(PageList.query.filter_by(id=2).one())
        db.session.commit()

        p = Page.query.count()
        pl = PageList.query.count()

        self.assertEqual(p, 5)
        self.assertEqual(pl, 0)


TEST_SUITE = make_test_suite(PagesListTest,)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
