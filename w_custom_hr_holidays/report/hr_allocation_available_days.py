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
    department_id = fields.Many2one(
        'hr.department', string='Department', readonly=True)
    number_day_allocation = fields.Float('Assigned days', readonly=True)
    used_request_day = fields.Float('Used days', readonly=True)
    remaining_days = fields.Float('Remaining days', readonly=True)
    holiday_status_id = fields.Many2one(
        'hr.leave.type', string='Leave Type', readonly=True)
    expiration = fields.Date(string='Expiration', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_allocation_available_days')
        self._cr.execute("""
            CREATE or REPLACE view hr_allocation_available_days as (
            WITH OPER AS (
            SELECT
                row_number() over(ORDER BY allocation.id) AS id,
                allocation.holiday_status_id AS holiday_status_id,
                allocation.employee_id AS employee_id,
                allocation.name AS name,
                allocation.vencimiento AS expiration,
                allocation.department_id AS department_id,
                allocation.number_of_days AS number_day_allocation,
                    sum(CASE
                        WHEN leave.holiday_status_id IS null OR leave.state!='validate' THEN 0
                        ELSE leave.number_of_days * -1
                    END) AS used_request_day
            FROM hr_leave_allocation AS allocation
            LEFT JOIN hr_leave AS leave
            ON leave.holiday_status_id=allocation.holiday_status_id AND leave.employee_id=allocation.employee_id
group by allocation.id,allocation.holiday_status_id, allocation.employee_id, allocation.name, allocation.vencimiento, allocation.department_id,allocation.number_of_days)
            SELECT 
            id, employee_id, holiday_status_id, name, department_id, number_day_allocation, used_request_day, (number_day_allocation + used_request_day) AS remaining_days, expiration FROM OPER
            group by id, holiday_status_id, employee_id, department_id, name, number_day_allocation, used_request_day, remaining_days,expiration)""")
