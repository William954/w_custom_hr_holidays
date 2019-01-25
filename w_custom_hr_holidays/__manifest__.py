# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution
########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################
{
    'name': 'Hr holidays custom',
    'author': 'TVP',
    'category': 'Extra Tools',
    'sequence': 50,
    'summary': "TVP",
    'version': '1.0',
    'description': """
Hr holidays custom
---------------------------
This module creates a report of the remaining days by absence assignments.
        """,
    'depends': [
        'base',
        'hr_holidays',
        'rh_tvp'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/inherit_hr_holidays_view.xml',
        'report/hr_allocation_report_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
}