# import tb_conexion
import json
from datetime import datetime

from odoo import fields, models

from .TbConexion import api_get_resourceid


class ResCompany(models.Model):
    _inherit = "res.company"

    resourceId = fields.Char(string="ResourceId", readonly="True")
    token = fields.Char(string="Token")
    turbodega_sync = fields.Boolean(string="Sync", default=False)
    turbodega_sync_date = fields.Datetime("datetime")

    def obtain_resourceId(self):
        for record in self:
            record.resourceId = ""
            tb_data = {}
            # print("record.token", record.token)
            return_value, json_message = api_get_resourceid(tb_data, record.token)
            # print("return_value", return_value)
            # print("json_message", json_message)
            if return_value:
                json_data = json.loads(json_message)
                record.resourceId = json_data["resourceId"]
                record.turbodega_sync = True
                record.turbodega_sync_date = datetime.now()
