# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2016- Vizucom Oy (http://www.vizucom.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Hitrate Report',
    'category': 'Sales',
    'version': '0.1',
    'author': 'Vizucom Oy',
    'depends': ['sale'],
    'description': """
Hitrate Report
==================
 * Adds the ability to create hitrate reports (i.e. how many quotations have become sale orders) for a selected timespan
 * Contains just the OpenERP views, a PDF print is created separately with Aeroo Reports

""",
    'data': [
    	'views/hitrate_report.xml',
    ],
}
