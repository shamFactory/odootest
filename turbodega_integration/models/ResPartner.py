# import tb_conexion
import time

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .TbConexion import api_send_partner, api_update_partner


class ResPartner(models.Model):
    _inherit = "res.partner"

    turbodega_sync = fields.Boolean(string="Sync", default=False)
    turbodega_sync_date = fields.Datetime("datetime")
    turbodega_creation = fields.Boolean(string="Create", default=False)
    dniresponsable = fields.Char(string="Dni responsable")

    def api_send(self, tb_data):
        return api_send_partner(tb_data, self.env.company.token)

    def api_update_product(self, tb_data):
        return api_update_partner(tb_data, self.env.company.token)

    @api.model
    def create(self, vals):
        result = super(ResPartner, self).create(vals)
        if not vals["country_id"]:
            raise UserError(_("Necesita especificar un país."))
        self.env["sync.api"].sync_api(id_product=result.id, model="res.partner")
        time.sleep(1)
        return result

    def write(self, vals):
        result = super(ResPartner, self).write(vals)
        if self.to_json_validation(
            vals,
            [
                "street_name",
                "country_id",
                "partner_latitude",
                "partner_longitude",
                "state_id",
                "zip",
                "tb_geocoord",
                "name",
                "mobile",
                "industry_id",
                "comment",
                "l10n_latam_identification_type_id",
                "vat",
            ],
        ):
            self.env["sync.api"].sync_update(self.id, model="res.partner")
        return result

    def to_json_turbodega(self):
        partner_1 = self.env["res.partner"].browse(self.id)
        tb_geocoord = [partner_1.partner_latitude, partner_1.partner_longitude]
        tb_address = {
            "street": partner_1.street_name,
            "town": partner_1.state_id.name or "",
            "postalCode": partner_1.zip or "",
            "adminDivision": False,
            "countryCode": partner_1.country_id.code,
            "geocoord": tb_geocoord,
        }
        doc_ruc = ""
        doc_dni = ""
        if self.l10n_latam_identification_type_id.name == "RUC":
            doc_ruc = self.vat
            doc_dni = ""
        if self.l10n_latam_identification_type_id.name == "DNI":
            doc_ruc = ""
            doc_dni = self.vat

        tb_data = {
            "code": str(partner_1.id).zfill(5),
            "name": partner_1.name,
            "address": tb_address,
            "dni": doc_dni,
            "ruc": doc_ruc,
            "mobile": partner_1.mobile or "",
            "businessType": partner_1.industry_id.name or False,
            "notes": partner_1.comment or "",
        }
        return tb_data

    def to_json_validation(self, vals, list_values):
        for data in list_values:
            if vals.get(data, False):
                return True
        return False
