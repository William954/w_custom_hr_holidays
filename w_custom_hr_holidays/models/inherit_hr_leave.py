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
from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def _read_from_database(self, field_names, inherited_field_names=[]):
        res = super(HrLeave, self)._read_from_database(
            field_names, inherited_field_names)
        if 'name' in field_names:
            for record in self:
                try:
                    sql = """
                        SELECT name 
                        FROM hr_leave
                        WHERE id={}""".format(record.id)
                    self._cr.execute(sql)
                    if self._cr.rowcount > 0:
                        res = self._cr.fetchone()[0]
                        if res is None or res is False:
                            res = ''
                    record._cache['name']
                    record._cache['name'] = res
                    print( record._cache['name'])
                except Exception:
                    # skip SpecialValue (e.g. for missing record or access right)
                    pass
        return res