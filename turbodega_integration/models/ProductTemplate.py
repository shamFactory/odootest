import logging

from odoo import api, fields, models

from .TbConexion import api_send_product, api_update_product

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    turbodega_sync = fields.Boolean(string="Sync", default=False)
    turbodega_creation = fields.Boolean(string="Create", default=False)
    turbodega_sync_date = fields.Datetime("datetime")
    turbodega_type_entity = fields.Selection(
        [
            ("turbodega", "Tienda turbodega"),
            ("otro", "Otro"),
        ],
        "Tipo",
        required=True,
        default="turbodega",
    )

    company_id_turbodega = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id,
    )
    resultado = fields.Text(string="Result", readonly="True")

    def api_send(self, tb_data):
        return api_send_product(tb_data, self.env.company.token)

    def api_update_product(self, tb_data):
        return api_update_product(tb_data, self.env.company.token)

    def to_json_turbodega(self):
        producto_1 = self.env["product.template"].browse(self.id)
        producto_product_1 = self.env["product.product"].search(
            [("product_tmpl_id", "=", self.id)]
        )
        _logger.error(producto_product_1)
        _logger.error(producto_product_1[0].name)
        pricelist_1 = self.env["product.pricelist.item"].search(
            [("product_tmpl_id", "=", self.id)]
        )
        prices_lines = []
        if pricelist_1:
            for line in pricelist_1:
                tb_prices = {
                    "maxQuantity": 0,
                    "minQuantity": 0,
                    "default": 0,
                    "price": line.fixed_price,
                }
                prices_lines.append(tb_prices)
        tb_data = {}
        # stock_level = "-"
        # if producto_1.type == "product":
        stock_level = producto_1.qty_available
        tb_data = {
            "resourceId": self.env.company.resourceId,
            # "distributorSKU": str(producto_1.id).zfill(5),
            "distributorSKU": str(producto_product_1.id).zfill(5),
            "distributorProductId": producto_1.default_code,
            "openerp_product_uom": producto_1.uom_id.id,
            "name": producto_1.name,
            "displayName": producto_1.name or "",
            "description": producto_1.description or "",
            "manufacturer": producto_1.manufacturer.name or "",
            "brand": producto_1.product_brand_id.name or "",
            # "stockLevel": producto_1.qty_available,
            "stockLevel": stock_level,
            "price": producto_1.list_price,  # el precio sugerido al cliente
            "prices": prices_lines or False,
            "salesUnitPrice": producto_1.list_price,
            "salesUnitType": producto_1.uom_id.name or False,
            "salesUnitPerBox": False,
            "weight": producto_1.weight,
            "currency": producto_1.currency_id.name,
        }
        if producto_1.list_price:
            tb_data["prices"] = prices_lines
        return tb_data

    @api.model
    def create(self, vals):
        result = super(ProductTemplate, self).create(vals)
        self.env["sync.api"].sync_api(id_product=result.id, model="product.template")
        return result

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        _logger.info(vals)
        if self.to_json_validation(
            vals,
            [
                "default_code",
                "uom_id",
                "name",
                "description",
                "manufacturer",
                "product_brand_id",
                "list_price",
                "weight",
                "currency_id",
                "qty_available",
            ],
        ):
            self.env["sync.api"].sync_update(self.id, model="product.template")
        return result

    def scheduler_1minute(self):
        list_productos = self.env["product.template"].search(
            [("turbodega_creation", "=", False)]
        )
        for data in list_productos:
            self.env["sync.api"].sync_api(id_product=data.id, model="product.template")

        list_productos = self.env["product.template"].search(
            [("turbodega_sync", "=", False)]
        )
        for data in list_productos:
            self.env["sync.api"].sync_update(
                id_product=data.id, model="product.template"
            )

    def sync_turbodega(self):

        for record in self:
            self.env["sync.api"].sync_api(
                id_product=record.id, model="product.template"
            )

    def to_json_validation(self, vals, list_values):
        for data in list_values:
            if vals.get(data, False):
                return True
        return False
