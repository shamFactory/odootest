# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Jarsa Sistemas (Sarai Osorio <sarai.osorio@jarsa.com.mx>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def create(self, vals):
        result = super(StockMoveLine, self).create(vals)
        self.product_id.turbodega_sync = False
        _logger.warn("create")
        _logger.warn(vals)
        _logger.warn(self.product_id)
        return result

    def write(self, vals):
        result = super(StockMoveLine, self).write(vals)
        _logger.warn("update")
        _logger.warn(vals)
        _logger.warning(self.product_id.name)
        self.product_id.turbodega_sync = False
        return result