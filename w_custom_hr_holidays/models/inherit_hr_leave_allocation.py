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
from dateutil.relativedelta import relativedelta


class LeaveReport(models.Model):
    _inherit = "hr.leave.report"

    expiration = fields.Date(string='Expiration', readonly=True)
    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_report')
        print("entro al supeeeeeeeeeeeeeeeeeeeeeer")
        self._cr.execute("""
            CREATE or REPLACE view hr_leave_report as (
            SELECT row_number() over(ORDER BY leaves.employee_id) as id,
                leaves.employee_id as employee_id, leaves.name as name,
                leaves.number_of_days as number_of_days, leaves.type as type,
                leaves.category_id as category_id, leaves.department_id as department_id,
                leaves.holiday_status_id as holiday_status_id, leaves.state as state,
                leaves.holiday_type as holiday_type, leaves.date_from as date_from,
                leaves.date_to as date_to, leaves.payslip_status as payslip_status, leaves.expiration as expiration
                from (select
                    allocation.employee_id as employee_id,
                    allocation.name as name,
                    allocation.number_of_days as number_of_days,
                    allocation.category_id as category_id,
                    allocation.department_id as department_id,
                    allocation.holiday_status_id as holiday_status_id,
                    allocation.state as state,
                    allocation.holiday_type,
                    null as date_from,
                    null as date_to,
                    FALSE as payslip_status,
                    'allocation' as type,
                    allocation.vencimiento as expiration
                from hr_leave_allocation as allocation
                union all select
                    request.employee_id as employee_id,
                    request.name as name,
                    (request.number_of_days * -1) as number_of_days,
                    request.category_id as category_id,
                    request.department_id as department_id,
                    request.holiday_status_id as holiday_status_id,
                    request.state as state,
                    request.holiday_type,
                    request.date_from as date_from,
                    request.date_to as date_to,
                    request.payslip_status as payslip_status,
                    'request' as type,
                    null as expiration
                from hr_leave as request) leaves
            );
        """)


class leaveasignations(models.Model):
    _inherit = 'hr.leave.allocation'


    vencimiento = fields.Date(
        store=True,
        string='Vencimiento',
        compute='_cumple_laboral_calcution')


    @api.one
    @api.depends('date_in','comple_laboral','antiquity','validity')
    def _cumple_laboral_calcution(self):
        if self.date_in:
            self.comple_laboral = fields.Date.from_string(
                self.date_in) + relativedelta(years=self.antiquity)
            self.vencimiento = fields.Date.from_string(
                self.comple_laboral) + relativedelta(months=self.validity)