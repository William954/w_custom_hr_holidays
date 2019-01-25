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
from odoo import api, fields, models, tools


class HrAllocationAvailableDays(models.Model):
    _name = "hr.allocation.available.days"
    _description = 'Available days'
    _auto = False
    _order = "employee_id"

    employee_id = fields.Many2one(
        'hr.employee', string="Employee", readonly=True)
    name = fields.Char('Description', readonly=True)
    number_of_days = fields.Float('Assigned days', readonly=True)
    used_days = fields.Float('Used days', readonly=True)
    remaining_days = fields.Float('Remaining days', readonly=True)
    type = fields.Selection([
        ('allocation', 'Allocation Request'),
        ('request', 'Leave Request')
        ], string='Request Type', readonly=True)
    department_id = fields.Many2one(
        'hr.department', string='Department', readonly=True)
    category_id = fields.Many2one(
        'hr.employee.category', string='Employee Tag', readonly=True)
    holiday_status_id = fields.Many2one(
        'hr.leave.type', string='Leave Type', readonly=True)
    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('category', 'By Employee Tag')
    ], string='Allocation Mode', readonly=True)
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True)
    expiration = fields.Date(string='Expiration', readonly=True)


    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_allocation_available_days')
        self._cr.execute("""
            CREATE or REPLACE view hr_allocation_available_days as (
            SELECT  DISTINCT
                row_number() over(ORDER BY allocation.employee_id) AS id,
                allocation.id AS allocation_id,
                allocation.employee_id AS employee_id,
                allocation.name AS name,
                allocation.number_of_days AS number_of_days,
                sum((request.number_of_days) * -1) AS used_days,
                ((allocation.number_of_days) + SUM(request.number_of_days) * -1) AS remaining_days,
                allocation.category_id AS category_id,
                allocation.department_id AS department_id,
                allocation.holiday_status_id AS holiday_status_id,
                allocation.state AS state,
                allocation.vencimiento AS expiration,
                allocation.holiday_type,
                'allocation' AS type
            FROM hr_leave_allocation AS allocation
            JOIN hr_leave AS request
            ON request.holiday_status_id = allocation.holiday_status_id
            JOIN hr_employee AS hr
            ON hr.id = allocation.employee_id AND hr.id =request.employee_id
            GROUP BY allocation_id, allocation.holiday_status_id
            );
        """)
