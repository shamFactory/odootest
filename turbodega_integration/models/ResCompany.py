# import tb_conexion
import json
import logging
from datetime import datetime

from odoo import fields, models

from .TbConexion import api_get_resourceid

_logger = logging.getLogger(__name__)


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
            return_value, json_message = api_get_resourceid(tb_data, record.token)
            if return_value:
                json_data = json.loads(json_message)
                record.resourceId = json_data["resourceId"]
                record.turbodega_sync = True
                record.turbodega_sync_date = datetime.now()
