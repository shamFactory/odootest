from odoo import fields, models


class LogsRequest(models.Model):
    _description = "Error log"
    _name = "logs.request"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Name", required=False, track_visibility="always")
    # web_service = fields.Char(string="WebService", track_visibility='always')
    model_type = fields.Char(string="model", track_visibility="always")
    type_operation = fields.Char(string="type_operation", track_visibility="always")
    # referencia_deuda = fields.Char(string="Socio", track_visibility='always')
    # numero_documento = fields.Char(string="Documento", track_visibility='always')
    fechaOperacion = fields.Char(string="fechaOperacion", track_visibility="always")
    # horaOperacion = fields.Char(string="horaOperacion", track_visibility='always')

    json_in = fields.Text(string="Json IN", track_visibility="always")
    json_out = fields.Text(string="Json OUT", track_visibility="always")
    error_details = fields.Char(string="Error details", track_visibility="always")

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.user.company_id,
        index=True,
    )
    stages_id = fields.Selection(
        [("new", "Nuevo"), ("done", "Ejecutado"), ("error", "Error")], default="new"
    )
